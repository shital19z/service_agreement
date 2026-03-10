"""fix zip and initials column lengths

Revision ID: c04cd39264de
Revises: 517033612724
Create Date: 2026-03-07 13:04:54.746743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c04cd39264de'
down_revision: Union[str, Sequence[str], None] = '517033612724'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
