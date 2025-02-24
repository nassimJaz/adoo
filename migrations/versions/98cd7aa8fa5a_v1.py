"""V1

Revision ID: 98cd7aa8fa5a
Revises: 
Create Date: 2025-02-18 18:24:29.319535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98cd7aa8fa5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projet',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('titre', sa.String(length=100), nullable=False),
    sa.Column('objectifs', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('date_debut', sa.DateTime(), nullable=False),
    sa.Column('date_fin_prevue', sa.DateTime(), nullable=False),
    sa.Column('statut', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utilisateur',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('mot_de_passe', sa.String(length=128), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=False),
    sa.Column('prenom', sa.String(length=64), nullable=False),
    sa.Column('a_propos', sa.Text(), nullable=True),
    sa.Column('preferences_notif', sa.String(length=20), nullable=True),
    sa.Column('date_inscription', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_utilisateur_email'), ['email'], unique=True)

    op.create_table('commentaire',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('contenu', sa.Text(), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('auteur_id', sa.String(length=36), nullable=False),
    sa.Column('projet_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['auteur_id'], ['utilisateur.id'], ),
    sa.ForeignKeyConstraint(['projet_id'], ['projet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('project_id', sa.String(length=36), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('contenu', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projet_membre',
    sa.Column('id_projet_membre', sa.String(length=36), nullable=False),
    sa.Column('projet_id', sa.String(length=36), nullable=True),
    sa.Column('utilisateur_id', sa.String(length=36), nullable=True),
    sa.Column('createur_id', sa.String(length=36), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('date_ajout', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['projet_id'], ['projet.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id_projet_membre')
    )
    op.create_table('tache',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('titre', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('date_echeance', sa.DateTime(), nullable=False),
    sa.Column('priorite', sa.String(length=20), nullable=False),
    sa.Column('statut', sa.String(length=20), nullable=True),
    sa.Column('projet_id', sa.String(length=36), nullable=False),
    sa.Column('responsable_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['projet_id'], ['projet.id'], ),
    sa.ForeignKeyConstraint(['responsable_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tache')
    op.drop_table('projet_membre')
    op.drop_table('notifications')
    op.drop_table('commentaire')
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_utilisateur_email'))

    op.drop_table('utilisateur')
    op.drop_table('projet')
    # ### end Alembic commands ###
