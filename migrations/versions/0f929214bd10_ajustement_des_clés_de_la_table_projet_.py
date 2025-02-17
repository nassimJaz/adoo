"""ajustement des clés de la table projet_membre

Revision ID: 0f929214bd10
Revises: e884860b49fb
Create Date: 2025-02-17 10:49:45.127041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f929214bd10'
down_revision = 'e884860b49fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projet_membre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_projet_membre', sa.Integer(), nullable=False))
        batch_op.alter_column('utilisateur_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)
        batch_op.alter_column('projet_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projet_membre', schema=None) as batch_op:
        batch_op.alter_column('projet_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
        batch_op.alter_column('utilisateur_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
        batch_op.drop_column('id_projet_membre')

    # ### end Alembic commands ###
