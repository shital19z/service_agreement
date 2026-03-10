"""manually remove varchar length restrictions

Revision ID: b69ca8404ddc
Revises: d0914bb31fcc
Create Date: 2026-03-07 12:13:07.961492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b69ca8404ddc'
down_revision: Union[str, Sequence[str], None] = 'd0914bb31fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
