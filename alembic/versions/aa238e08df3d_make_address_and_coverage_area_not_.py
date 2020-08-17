"""Make address and coverage_area not nullable

Revision ID: aa238e08df3d
Revises: f1215e1bc1d5
Create Date: 2020-08-17 04:07:37.867192

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa238e08df3d'
down_revision = 'f1215e1bc1d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('partner', 'address',
               existing_type=geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=False)
    op.alter_column('partner', 'coverage_area',
               existing_type=geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=False)
    op.drop_index('idx_partner_address', table_name='partner')
    op.drop_index('idx_partner_coverage_area', table_name='partner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_partner_coverage_area', 'partner', ['coverage_area'], unique=False)
    op.create_index('idx_partner_address', 'partner', ['address'], unique=False)
    op.alter_column('partner', 'coverage_area',
               existing_type=geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=True)
    op.alter_column('partner', 'address',
               existing_type=geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'),
               nullable=True)
    # ### end Alembic commands ###