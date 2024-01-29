from fastapi_injector import request_scope
from injector import (
    Binder,
    Module,
    provider,
    singleton,
)
from kiwi_amqp_client import AmqpClient

from housing_component.core.constants import AMQPRoutingKeys
from housing_component.core.db.client import DbClient
from housing_component.core.unit_of_work import UnitOfWork
from housing_component.settings import (
    AMQP_BROKER_HOST,
    AMQP_BROKER_PASSWORD,
    AMQP_BROKER_PORT,
    AMQP_BROKER_USERNAME,
    AMQP_BROKER_VIRTUAL_HOST,
    AMQP_EXCHANGE_NAME,
    AMQP_CONSUMER_QUEUE_NAME,
    AMQP_PREFETCH_COUNT,
    DB_ECHO,
    DB_URL,
)


class CoreModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(UnitOfWork, scope=request_scope)

    @singleton
    @provider
    def provide_db_client(self) -> DbClient:
        return DbClient(DB_URL, DB_ECHO)

    @singleton
    @provider
    def provide_amqp_client(self) -> AmqpClient:
        return AmqpClient(
            host=AMQP_BROKER_HOST,
            port=AMQP_BROKER_PORT,
            username=AMQP_BROKER_USERNAME,
            password=AMQP_BROKER_PASSWORD,
            virtualhost=AMQP_BROKER_VIRTUAL_HOST,
            exchange_name=AMQP_EXCHANGE_NAME,
            consumer_queue_name=AMQP_CONSUMER_QUEUE_NAME,
            consumer_routing_keys=list(AMQPRoutingKeys),
            prefetch_count=AMQP_PREFETCH_COUNT,
        )
