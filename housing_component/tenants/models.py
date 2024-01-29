from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from housing_component.core.db.models import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(63), primary_key=True)  # noqa: A003
    external_id: Mapped[str] = mapped_column(nullable=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), primary_key=True, nullable=False
    )
    email_address: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("external_id", "organization_id"),
        UniqueConstraint("email_address", "organization_id"),
        CheckConstraint(
            "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
            name="id_format_check",
        ),
    )

    def __repr__(self) -> str:
        return f"Tenant(id={self.id!r}, organization_id={self.organization_id!r})"
