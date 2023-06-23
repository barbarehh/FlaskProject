from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_todo = db.Column(db.String(300), nullable=False)
    mark_as_done = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"{self.id} and {self.create_todo}"
