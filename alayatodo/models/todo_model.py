from alayatodo import db
from alayatodo.models.user_model import User


class Todo(db.Model):
    __tablename__ = 'todos'
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description, user_id):
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return "Description: {description}".format(description=self.description)