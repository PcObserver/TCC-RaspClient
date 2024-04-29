"""empty message

Revision ID: 499689ce5a59
Revises: 
Create Date: 2024-04-21 15:21:48.974261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '499689ce5a59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('device_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('brand_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('user_devices', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('device_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('device_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('device_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('user_devices', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('device_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.alter_column('brand_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('actions', schema=None) as batch_op:
        batch_op.alter_column('device_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    # ### end Alembic commands ###