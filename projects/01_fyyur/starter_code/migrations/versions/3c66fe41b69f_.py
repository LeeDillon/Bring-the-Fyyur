"""empty message

Revision ID: 3c66fe41b69f
Revises: e21a464fe450
Create Date: 2023-02-14 17:51:16.912169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c66fe41b69f'
down_revision = 'e21a464fe450'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###
