from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from housing_component.core.db.models import Base


class RentalUnit(Base):
    __tablename__ = "rental_unit"

    id: Mapped[str] = mapped_column(String(63), primary_key=True)  # noqa: A003
    external_id: Mapped[str] = mapped_column(nullable=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[Optional[str]] = mapped_column(
        ForeignKey("addresses.id"), nullable=True
    )  # Set nullable to True
    address_rel = relationship("Address")
    access_point_rel = relationship(
        "AccessPoint", back_populates="rental_unit_rel", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("external_id", "organization_id"),
        CheckConstraint(
            "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
            name="id_format_check",
        ),
    )

    def __repr__(self) -> str:
        return f"RentalUnit(id={self.id!r}, organization_id={self.organization_id!r})"
