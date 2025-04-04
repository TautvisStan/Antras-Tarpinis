"""vartotojo patvirtinimas

Revision ID: 00f24221aaa0
Revises: f3230e1035ab
Create Date: 2025-03-19 14:21:35.717638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f24221aaa0'
down_revision = 'f3230e1035ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('el_pat', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('el_pat_data', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('dest_pat', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('dest_pat_data', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.drop_column('dest_pat_data')
        batch_op.drop_column('dest_pat')
        batch_op.drop_column('el_pat_data')
        batch_op.drop_column('el_pat')

    # ### end Alembic commands ###
