from backend.core.bootstrap import Bootstrap
from backend.core.messagebus_handler import MessageBus

from ..infra.handlers import (
    EVENTS_HANDLERS_FOR_INJECTION, COMMANDS_HANDLERS_FOR_INJECTION
)
from ..infra.uow.sqlalchemy.attraction_uow import (
    SQLAlchemyAttractionsUnitOfWork
)


def get_message_bus() -> MessageBus:
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyAttractionsUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )
    print("get message bus")
    messagebus: MessageBus = bootstrap.get_messagebus()
    print(f"messbus: {messagebus}")
    return messagebus


messagebus = get_message_bus()
