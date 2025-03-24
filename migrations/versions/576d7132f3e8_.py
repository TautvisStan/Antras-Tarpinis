"""empty message

Revision ID: 576d7132f3e8
Revises: 2dff5593abac
Create Date: 2025-03-24 13:32:31.502716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '576d7132f3e8'
down_revision = '2dff5593abac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('uzduotys',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pavadinimas', sa.String(length=80), nullable=True),
    sa.Column('data_nuo', sa.DateTime(timezone=50), nullable=False),
    sa.Column('data_iki', sa.DateTime(timezone=50), nullable=False),
    sa.Column('aprasymas', sa.String(length=50), nullable=False),
    sa.Column('modulis_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['modulis_id'], ['moduliai.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('studento_pasiekimai',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('studentas_id', sa.Integer(), nullable=False),
    sa.Column('paskaita_id', sa.Integer(), nullable=False),
    sa.Column('pazymys', sa.Integer(), nullable=True),
    sa.Column('nedalyvavo', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['paskaita_id'], ['paskaitos.id'], ),
    sa.ForeignKeyConstraint(['studentas_id'], ['vartotojai.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('studento_pasiekimai')
    op.drop_table('uzduotys')
    # ### end Alembic commands ###
