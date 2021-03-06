"""create invoices table

Revision ID: e4d55a3a4ee4
Revises: e9cc76f8a4b1
Create Date: 2022-03-07 18:02:12.463404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4d55a3a4ee4'
down_revision = 'e9cc76f8a4b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoices', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.alter_column('invoices', 'invoiceNum',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('invoices', 'invoiceDate',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('invoices', 'invoiceDue',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('invoices', 'invoiceAmountDue',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'invoiceAmountDue',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('invoices', 'invoiceDue',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('invoices', 'invoiceDate',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('invoices', 'invoiceNum',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('invoices', 'created_at')
    # ### end Alembic commands ###