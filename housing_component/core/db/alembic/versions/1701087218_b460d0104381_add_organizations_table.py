"""add organizations table

Revision ID: b460d0104381
Revises: 
Create Date: 2023-11-27 13:13:38.919452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b460d0104381"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("organizations")
    # ### end Alembic commands ###
