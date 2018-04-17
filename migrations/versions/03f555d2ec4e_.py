"""empty message

Revision ID: 03f555d2ec4e
Revises: 0204235987b0
Create Date: 2018-04-12 18:24:23.026435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03f555d2ec4e'
down_revision = '0204235987b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'tables', 'establishments', ['establishment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tables', type_='foreignkey')
    # ### end Alembic commands ###
