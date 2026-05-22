"""allow contact email gender null

Revision ID: a4f2d8c9b713
Revises: 678e293cb579
Create Date: 2026-05-22 15:30:00.000000

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a4f2d8c9b713"
down_revision = "678e293cb579"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("contact_emails", schema=None) as batch_op:
        batch_op.alter_column(
            "gender",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade():
    with op.batch_alter_table("contact_emails", schema=None) as batch_op:
        batch_op.alter_column(
            "gender",
            existing_type=sa.Integer(),
            nullable=False,
        )
