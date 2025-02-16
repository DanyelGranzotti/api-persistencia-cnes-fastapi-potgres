from alembic import op
import sqlalchemy as sa

revision = 'create_estabelecimento_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'estabelecimentos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo_unidade', sa.String(20), nullable=False),
        sa.Column('codigo_cnes', sa.String(20), nullable=False),
        sa.Column('cnpj_mantenedora', sa.String(14), nullable=False),
        sa.Column('nome_razao_social_estabelecimento', sa.String(255), nullable=False),
        sa.Column('nome_fantasia_estabelecimento', sa.String(255), nullable=False),
        sa.Column('numero_telefone_estabelecimento', sa.String(20), nullable=True),
        sa.Column('email_estabelecimento', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo_unidade'),
        sa.UniqueConstraint('codigo_cnes')
    )

def downgrade() -> None:
    op.drop_table('estabelecimentos')
