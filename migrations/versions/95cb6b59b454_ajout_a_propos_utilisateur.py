"""ajout a propos utilisateur

Revision ID: 95cb6b59b454
Revises: 272412ef3a4c
Create Date: 2025-02-18 00:10:21.941961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95cb6b59b454'
down_revision = '272412ef3a4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.add_column(sa.Column('a_propos', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.drop_column('a_propos')

    # ### end Alembic commands ###
