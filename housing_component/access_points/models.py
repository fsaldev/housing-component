from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from housing_component.access_points.schemas import PermissionEnum
from housing_component.core.db.models import Base
from sqlalchemy.dialects.postgresql import ENUM


class AccessPoint(Base):
    __tablename__ = "access_point"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(nullable=True)
    rental_unit_id: Mapped[str] = mapped_column()
    organization_id: Mapped[int] = mapped_column()
    permission: Mapped[PermissionEnum] = mapped_column(
        ENUM(PermissionEnum), default=PermissionEnum.IS_HOST
    )

    rental_unit_rel = relationship("RentalUnit", back_populates="access_point_rel")

    __table_args__ = (
        ForeignKeyConstraint(
            ["rental_unit_id", "organization_id"],
            ["rental_unit.id", "rental_unit.organization_id"],
        ),
    )

    def __repr__(self) -> str:
        return f"AccessPoint(id={self.id!r}, permission={self.permission!r})"
