from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    UniqueConstraint,
    String,
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from housing_component.core.db.models import Base
from uuid import UUID


class RentalAgreement(Base):
    __tablename__ = "rental_agreement"

    id: Mapped[str] = mapped_column(String(63), primary_key=True)  # noqa: A003
    external_id: Mapped[str] = mapped_column(nullable=True)
    organization_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    tenant_id: Mapped[str] = mapped_column()
    rental_unit_id: Mapped[str] = mapped_column()
    start_at: Mapped[datetime] = mapped_column(
        nullable=False,
        type_=DateTime(timezone=True),
    )
    end_at: Mapped[datetime] = mapped_column(
        nullable=False,
        type_=DateTime(timezone=True),
    )
    state: Mapped[UUID] = mapped_column(ForeignKey("states.id"), nullable=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "organization_id"], ["tenants.id", "tenants.organization_id"]
        ),
        ForeignKeyConstraint(
            ["rental_unit_id", "organization_id"],
            ["rental_unit.id", "rental_unit.organization_id"],
        ),
        UniqueConstraint("id", "organization_id"),
        UniqueConstraint("external_id", "organization_id"),
        CheckConstraint(
            "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
            name="id_format_check",
        ),
    )
    tenant_rel = relationship("Tenant")
    state_rel = relationship("State")
    rental_unit_rel = relationship("RentalUnit")

    def __repr__(self) -> str:
        return (
            f",RentalAgreement(id={self.id!r},"
            f" tenant_id={self.tenant_id!r},"
            f" state={self.state!r},"
            f" organization_id={self.organization_id!r})"
        )
