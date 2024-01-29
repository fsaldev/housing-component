from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from housing_component.core.db.models import Base
from sqlalchemy.dialects.postgresql import ENUM
from housing_component.state.schemas import (
    DesiredStateEnum,
    ActualStateEnum,
    StatusEnum,
)


class State(Base):
    __tablename__ = "states"
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)  # noqa: A003
    desired: Mapped[DesiredStateEnum] = mapped_column(ENUM(DesiredStateEnum))
    actual: Mapped[ActualStateEnum] = mapped_column(
        ENUM(ActualStateEnum), default=ActualStateEnum.Created
    )
    error: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[StatusEnum] = mapped_column(ENUM(StatusEnum), default=StatusEnum.OK)

    def __repr__(self) -> str:
        return f",State(id={self.id!r},"
