"""fix zip and initials column lengths

Revision ID: xxxxx
Revises: 517033612724
Create Date: 2026-03-07 12:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'xxxxx'  # This will be auto-generated
down_revision = '517033612724'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Remove length limits from zip code columns
    op.alter_column('agreements', 'care_zip',
                    existing_type=sa.String(length=10),
                    type_=sa.String(),
                    existing_nullable=True)
    
    op.alter_column('agreements', 'clt_zip',
                    existing_type=sa.String(length=10),
                    type_=sa.String(),
                    existing_nullable=True)
    
    # Remove length limit from client_initials
    op.alter_column('agreements', 'client_initials',
                    existing_type=sa.String(length=5),
                    type_=sa.String(),
                    existing_nullable=True)
    
    # Note: branch_code (50) and perc_charged (10) are kept as is

def downgrade() -> None:
    # Put the limits back (if needed)
    op.alter_column('agreements', 'care_zip',
                    existing_type=sa.String(),
                    type_=sa.String(length=10),
                    existing_nullable=True)
    
    op.alter_column('agreements', 'clt_zip',
                    existing_type=sa.String(),
                    type_=sa.String(length=10),
                    existing_nullable=True)
    
    op.alter_column('agreements', 'client_initials',
                    existing_type=sa.String(),
                    type_=sa.String(length=5),
                    existing_nullable=True)