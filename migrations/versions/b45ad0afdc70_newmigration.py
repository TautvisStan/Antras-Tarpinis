"""newMigration

Revision ID: b45ad0afdc70
Revises: 7f6bdc3d5a03
Create Date: 2025-03-20 19:16:14.797188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b45ad0afdc70'
down_revision = '7f6bdc3d5a03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tvarkarasciai',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('savaites_diena', sa.Integer(), nullable=False),
    sa.Column('pakaitos_pavadinimas', sa.String(length=50), nullable=False),
    sa.Column('laikas_nuo', sa.Time(), nullable=False),
    sa.Column('laikas_iki', sa.Time(), nullable=False),
    sa.Column('uzduotis_id', sa.Integer(), nullable=True),
    sa.Column('atsiskaitymas_id', sa.Integer(), nullable=True),
    sa.Column('modulis_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atsiskaitymas_id'], ['atsiskaitymai.id'], ),
    sa.ForeignKeyConstraint(['modulis_id'], ['moduliai.id'], ),
    sa.ForeignKeyConstraint(['uzduotis_id'], ['uzduotys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('paskaitos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipas', sa.String(length=50), nullable=False))

    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ikelimo_data', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('aktyvumas', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.drop_column('aktyvumas')
        batch_op.drop_column('ikelimo_data')

    with op.batch_alter_table('paskaitos', schema=None) as batch_op:
        batch_op.drop_column('tipas')

    op.drop_table('tvarkarasciai')
    # ### end Alembic commands ###
