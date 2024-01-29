import logging
from typing import Any, Type, TypeVar

from fastapi_injector import RequestScopeFactory
from injector import Inject, Injector

from housing_component.core.unit_of_work import UnitOfWork
from housing_component.core.use_cases import UseCase, UseCaseHandler
from housing_component.organizations.use_cases import (
    CreateOrganization,
    DeleteOrganization,
)
from housing_component.core.constants import AMQPRoutingKeys

log = logging.getLogger(__name__)

UseCaseT = TypeVar("UseCaseT", bound=UseCase)


class UnexpectedMessageError(Exception):
    pass


class AmqpInHandler:
    def __init__(
        self,
        injector: Inject[Injector],
        request_scope_factory: Inject[RequestScopeFactory],
    ) -> None:
        self._injector = injector
        self._request_scope_factory = request_scope_factory

    async def handle(self, payload: Any, routing_key: str | None) -> None:
        try:
            use_case = self._get_use_case(payload, routing_key)

        except UnexpectedMessageError:
            log.warn(
                "Received unexpected AMQP message. Message payload: %(payload)s",
                dict(payload=payload),
            )
            return
        except BaseException as e:
            log.error(
                "Failed to parse AMQP message. Error: %(exception)s. Message payload: %(payload)s",
                dict(exception=e, payload=payload),
            )
            return

        if use_case is None:
            return

        try:
            await self._execute_use_case(use_case)
        except BaseException as e:
            log.error(
                "Failed to handle AMQP message. Error: %(exception)s. Message payload: %(payload)s",
                dict(exception=e, payload=payload),
            )

    def _get_use_case(self, payload: Any, routing_key: str | None) -> UseCase | None:
        payload = payload["payload"]
        match routing_key:
            case AMQPRoutingKeys.AMQP_API_ORGANIZATIONS_CREATED_ROUTING_KEY:
                organization_id = payload["organization_id"]
                if organization_id is None:
                    log.warn(
                        "organization_id is None. Skipping processing of AMQP message. Message payload: %(payload)s",
                        dict(payload=payload),
                    )
                    return None

                return CreateOrganization(organization_id=organization_id)
            case AMQPRoutingKeys.AMQP_API_ORGANIZATIONS_DELETED_ROUTING_KEY:
                organization_id = payload["organization_id"]
                if organization_id is None:
                    log.warn(
                        "organization_id is None. Skipping processing of AMQP message. Message payload: %(payload)s",
                        dict(payload=payload),
                    )
                    return None

                return DeleteOrganization(organization_id=organization_id)

        raise UnexpectedMessageError()

    async def _execute_use_case(self, use_case: UseCaseT) -> None:
        async with self._request_scope_factory.create_scope():
            try:
                handler_cls: Type[UseCaseHandler[UseCaseT, Any]] = use_case.Handler  # type: ignore[attr-defined]
            except AttributeError:
                log.error(
                    "Failed to determine handler for %(use_case_type).",
                    dict(use_case_type=type(use_case)),
                )
                return

            handler = self._injector.get(handler_cls)
            async with self._injector.get(UnitOfWork):
                await handler.execute(use_case)
