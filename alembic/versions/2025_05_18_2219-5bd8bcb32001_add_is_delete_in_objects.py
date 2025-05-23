"""add is_delete in objects

Revision ID: 5bd8bcb32001
Revises: afa101316b78
Create Date: 2025-05-18 22:19:25.083186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bd8bcb32001'
down_revision: Union[str, None] = 'afa101316b78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'employees', ['id'])
    op.create_unique_constraint(None, 'groups', ['id'])
    op.create_unique_constraint(None, 'notifications', ['id'])
    op.add_column('objects', sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False))
    op.create_unique_constraint(None, 'objects', ['id'])
    op.create_unique_constraint(None, 'sanitary_breaks', ['id'])
    op.create_unique_constraint(None, 'sanitary_changes', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    op.create_unique_constraint(None, 'visit_history', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'visit_history', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'sanitary_changes', type_='unique')
    op.drop_constraint(None, 'sanitary_breaks', type_='unique')
    op.drop_constraint(None, 'objects', type_='unique')
    op.drop_column('objects', 'is_deleted')
    op.drop_constraint(None, 'notifications', type_='unique')
    op.drop_constraint(None, 'groups', type_='unique')
    op.drop_constraint(None, 'employees', type_='unique')
    # ### end Alembic commands ###
