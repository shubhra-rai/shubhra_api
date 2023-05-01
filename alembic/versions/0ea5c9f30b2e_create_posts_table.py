"""create posts table

Revision ID: 0ea5c9f30b2e
Revises: 
Create Date: 2023-04-28 20:41:10.317350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea5c9f30b2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
