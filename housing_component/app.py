import asyncio
from contextlib import asynccontextmanager
import logging
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from fastapi_injector import InjectorMiddleware, attach_injector
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector
from kiwi_amqp_client import AmqpClient

from housing_component.core.amqp_handler import AmqpInHandler
from housing_component.core.di import CoreModule
from housing_component.core.exceptions import (
    handle_internal_exception,
    handle_request_exception,
    handle_validation_exception,
    RequestException,
)
from housing_component.core.middleware import (
    UnitOfWorkMiddleware,
)
from housing_component.core.logging import setup_logging
from housing_component.core.routers import pre_router
from housing_component.core.schemas import Error
from housing_component.organizations.di import OrganizationModule
from housing_component.rental_units.di import RentalUnitsModule

setup_logging()
log = logging.getLogger(__name__)


injector = Injector([CoreModule(), OrganizationModule(), RentalUnitsModule()])

amqp_client = injector.get(AmqpClient)
amqp_consumer_task: None | asyncio.Task[Any] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global amqp_consumer_task

    log.info("Starting up...")
    await amqp_client.setup()
    amqp_consumer_task = asyncio.create_task(run_amqp_consumers())

    yield

    log.info("Shutting down...")
    if amqp_consumer_task and not amqp_consumer_task.done():
        amqp_consumer_task.cancel()
        try:
            await amqp_consumer_task
        except asyncio.CancelledError:
            pass

    await amqp_client.close()


app = FastAPI(
    title="KIWI.KI ERP Integration API",
    description="API that connects ERP integrations with the KIWI.KI backend",
    version="0.1.0",
    docs_url="/",
    responses={
        404: {
            "model": Error,
            "description": "Not Found",
        },
        422: {
            "model": Error,
            "description": "Validation Error",
        },
    },
    lifespan=lifespan,
)
attach_injector(app, injector)

app.add_middleware(UnitOfWorkMiddleware, injector=injector)
app.add_middleware(InjectorMiddleware, injector=injector)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pre_router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:
    return handle_validation_exception(exc)


@app.exception_handler(RequestException)
async def request_exception_handler(
    request: Request, exc: RequestException
) -> Response:
    return handle_request_exception(exc)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception) -> Response:
    return handle_internal_exception(exc)


async def run_amqp_consumers() -> None:
    amqp_handler = injector.get(AmqpInHandler)
    try:
        await amqp_client.consume(amqp_handler.handle)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        log.exception("Uncaught exception in the AMQP consumer", e)
