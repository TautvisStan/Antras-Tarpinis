"""fakultetai

Revision ID: 5c0121677ba4
Revises: 576d7132f3e8
Create Date: 2025-03-25 10:09:44.427477

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c0121677ba4'
down_revision = '576d7132f3e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fakultetai',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pavadinimas', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('specializacijos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pavadinimas', sa.String(length=50), nullable=False),
    sa.Column('fakultetas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fakultetas_id'], ['fakultetai.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('testai',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pavadinimas', sa.String(length=100), nullable=False),
    sa.Column('modulis_id', sa.Integer(), nullable=False),
    sa.Column('atsiskaitymas_id', sa.Integer(), nullable=True),
    sa.Column('testo_sukurejas', sa.Integer(), nullable=False),
    sa.Column('maksimalus_balas', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['atsiskaitymas_id'], ['atsiskaitymai.id'], ),
    sa.ForeignKeyConstraint(['modulis_id'], ['moduliai.id'], ),
    sa.ForeignKeyConstraint(['testo_sukurejas'], ['vartotojai.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rezultatai',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vartotojas_id', sa.Integer(), nullable=False),
    sa.Column('testas_id', sa.Integer(), nullable=False),
    sa.Column('rezultatas', sa.Integer(), nullable=False),
    sa.Column('atlikimo_data', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['testas_id'], ['testai.id'], ),
    sa.ForeignKeyConstraint(['vartotojas_id'], ['vartotojai.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('atsiskaitymai', schema=None) as batch_op:
        batch_op.alter_column('aprasymas',
               existing_type=mysql.VARCHAR(collation='utf8_lithuanian_ci', length=50),
               type_=sa.String(length=500),
               existing_nullable=False)
        batch_op.drop_index('id')

    with op.batch_alter_table('moduliai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fakultetas_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'fakultetai', ['fakultetas_id'], ['id'])

    with op.batch_alter_table('studiju_programos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('specializacija_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'specializacijos', ['specializacija_id'], ['id'])

    with op.batch_alter_table('uzduotys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tekstas', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('testas_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('atsakymas', sa.String(length=200), nullable=False))
        batch_op.drop_constraint('uzduotys_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'testai', ['testas_id'], ['id'])
        batch_op.drop_column('modulis_id')
        batch_op.drop_column('pavadinimas')
        batch_op.drop_column('data_iki')
        batch_op.drop_column('data_nuo')
        batch_op.drop_column('aprasymas')

    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fakultetas_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'fakultetai', ['fakultetas_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vartotojai', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('fakultetas_id')

    with op.batch_alter_table('uzduotys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('aprasymas', mysql.VARCHAR(collation='utf8_lithuanian_ci', length=50), nullable=False))
        batch_op.add_column(sa.Column('data_nuo', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('data_iki', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('pavadinimas', mysql.VARCHAR(collation='utf8_lithuanian_ci', length=80), nullable=True))
        batch_op.add_column(sa.Column('modulis_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('uzduotys_ibfk_1', 'moduliai', ['modulis_id'], ['id'])
        batch_op.drop_column('atsakymas')
        batch_op.drop_column('testas_id')
        batch_op.drop_column('tekstas')

    with op.batch_alter_table('studiju_programos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('specializacija_id')

    with op.batch_alter_table('moduliai', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('fakultetas_id')

    with op.batch_alter_table('atsiskaitymai', schema=None) as batch_op:
        batch_op.create_index('id', ['id'], unique=True)
        batch_op.alter_column('aprasymas',
               existing_type=sa.String(length=500),
               type_=mysql.VARCHAR(collation='utf8_lithuanian_ci', length=50),
               existing_nullable=False)

    op.drop_table('rezultatai')
    op.drop_table('testai')
    op.drop_table('specializacijos')
    op.drop_table('fakultetai')
    # ### end Alembic commands ###
