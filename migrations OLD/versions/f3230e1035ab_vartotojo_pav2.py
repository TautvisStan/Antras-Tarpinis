"""vartotojo pav2

Revision ID: f3230e1035ab
Revises: a65432f146b5
Create Date: 2025-03-19 08:13:26.490365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3230e1035ab'
down_revision = 'a65432f146b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profilio_pav', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.drop_column('profilio_pav')

    # ### end Alembic commands ###
