"""empty message

Revision ID: 78d6e7a00faf
Revises: e880400ea636
Create Date: 2019-03-22 15:17:51.979346

"""
from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers, used by Alembic.
from alayatodo import db
from alayatodo.models.user_model import User

revision = '78d6e7a00faf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    users = User.query.all()
    for user in users:
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db.session.commit()
    pass


def downgrade():
    pass
