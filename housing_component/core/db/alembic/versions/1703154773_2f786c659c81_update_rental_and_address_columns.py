"""update rental and address columns

Revision ID: 2f786c659c81
Revises: ec7a26efd77e
Create Date: 2023-12-21 15:32:53.201955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f786c659c81"
down_revision = "ec7a26efd77e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Alter existing columns in the 'addresses' table
    op.alter_column(
        "addresses",
        "street",
        existing_type=sa.String(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "postal_code",
        existing_type=sa.String(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "city",
        existing_type=sa.String(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "state",
        existing_type=sa.String(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "country",
        existing_type=sa.String(),
        type_=sa.VARCHAR(length=2),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "lat",
        existing_type=sa.Float(),
        type_=sa.FLOAT(asdecimal=True),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "lng",
        existing_type=sa.Float(),
        type_=sa.FLOAT(asdecimal=True),
        existing_nullable=True,
    )
    op.create_check_constraint("id_byte_limit", "addresses", "octet_length(id) <= 40")

    # Alter existing columns and add new constraints in the 'rental_unit' table
    op.alter_column(
        "rental_unit",
        "id",
        existing_type=sa.String(),
        type_=sa.String(length=63),
        existing_nullable=False,
    )
    op.alter_column(
        "rental_unit",
        "address",
        existing_type=sa.String(),
        nullable=True,
    )
    op.create_check_constraint(
        "id_format_check",
        "rental_unit",
        "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Revert changes made to the 'addresses' table
    op.alter_column(
        "addresses",
        "street",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "postal_code",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "city",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ... continue for other columns
    op.alter_column(
        "addresses",
        "state",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "country",
        existing_type=sa.VARCHAR(length=2),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "lat",
        existing_type=sa.FLOAT(asdecimal=True),
        type_=sa.Float(),
        existing_nullable=True,
    )
    op.alter_column(
        "addresses",
        "lng",
        existing_type=sa.FLOAT(asdecimal=True),
        type_=sa.Float(),
        existing_nullable=True,
    )
    op.drop_constraint("id_byte_limit", "addresses", type_="check")

    # Revert changes made to the 'rental_unit' table
    op.alter_column(
        "rental_unit",
        "id",
        existing_type=sa.String(length=63),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "rental_unit",
        "address",
        existing_type=sa.String(),
        nullable=False,
    )
    op.drop_constraint("id_format_check", "rental_unit", type_="check")
    # ### end Alembic commands ###
