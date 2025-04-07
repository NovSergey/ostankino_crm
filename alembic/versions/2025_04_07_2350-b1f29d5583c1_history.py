"""history

Revision ID: b1f29d5583c1
Revises: 68304fb4644d
Create Date: 2025-04-07 23:50:59.528374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1f29d5583c1'
down_revision: Union[str, None] = '68304fb4644d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'visit_history',
        'entry_time',
        server_default=sa.text('now()'),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'visit_history',
        'entry_time',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )