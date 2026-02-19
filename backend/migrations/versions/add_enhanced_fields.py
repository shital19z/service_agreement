"""add enhanced fields for multi-page PDF and branch config

Revision ID: a1b2c3d4e5f6
Revises: 72bd826de058
Create Date: 2026-02-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '72bd826de058'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new fields to branches table
    op.add_column('branches', sa.Column('notice_period_days', sa.Integer(), nullable=True, server_default='3'))
    op.add_column('branches', sa.Column('holiday_count', sa.Integer(), nullable=True, server_default='11'))
    op.add_column('branches', sa.Column('state_authority', sa.Text(), nullable=True))
    op.add_column('branches', sa.Column('manager_phone', sa.String(25), nullable=True))
    op.add_column('branches', sa.Column('pdf_margin_top', sa.Float(), nullable=True, server_default='0.4'))
    op.add_column('branches', sa.Column('pdf_margin_bottom', sa.Float(), nullable=True, server_default='0.4'))
    op.add_column('branches', sa.Column('pdf_margin_left', sa.Float(), nullable=True, server_default='0.4'))
    op.add_column('branches', sa.Column('pdf_margin_right', sa.Float(), nullable=True, server_default='0.4'))
    op.add_column('branches', sa.Column('footer_version_tag', sa.String(50), nullable=True))
    op.add_column('branches', sa.Column('requires_consumer_notice', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('branches', sa.Column('mileage_rate', sa.Float(), nullable=True, server_default='0.67'))
    
    # Add new fields to agreements table
    op.add_column('agreements', sa.Column('frequency_duration', sa.String(), nullable=True))
    op.add_column('agreements', sa.Column('vehicle_authorized', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('agreements', sa.Column('vehicle_authorization_initials', sa.String(10), nullable=True))
    op.add_column('agreements', sa.Column('medication_administration', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('agreements', sa.Column('page1_signature', sa.Text(), nullable=True))
    op.add_column('agreements', sa.Column('page2_signature', sa.Text(), nullable=True))
    op.add_column('agreements', sa.Column('page3_signature', sa.Text(), nullable=True))
    
    # Update mileage_rate default for agreements
    op.alter_column('agreements', 'mileage_rate', server_default='0.67')


def downgrade() -> None:
    """Downgrade schema."""
    # Remove fields from agreements table
    op.drop_column('agreements', 'page3_signature')
    op.drop_column('agreements', 'page2_signature')
    op.drop_column('agreements', 'page1_signature')
    op.drop_column('agreements', 'medication_administration')
    op.drop_column('agreements', 'vehicle_authorization_initials')
    op.drop_column('agreements', 'vehicle_authorized')
    op.drop_column('agreements', 'frequency_duration')
    
    # Remove fields from branches table
    op.drop_column('branches', 'mileage_rate')
    op.drop_column('branches', 'requires_consumer_notice')
    op.drop_column('branches', 'footer_version_tag')
    op.drop_column('branches', 'pdf_margin_right')
    op.drop_column('branches', 'pdf_margin_left')
    op.drop_column('branches', 'pdf_margin_bottom')
    op.drop_column('branches', 'pdf_margin_top')
    op.drop_column('branches', 'manager_phone')
    op.drop_column('branches', 'state_authority')
    op.drop_column('branches', 'holiday_count')
    op.drop_column('branches', 'notice_period_days')




