"""login

Revision ID: 598e7fed33dd
Revises: 28f060ea5803
Create Date: 2025-03-18 11:45:22.478387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '598e7fed33dd'
down_revision = '28f060ea5803'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('el_pastas', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.drop_column('password_hash')
        batch_op.drop_column('el_pastas')

    # ### end Alembic commands ###
