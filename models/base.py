from flask_sqlalchemy import SQLAlchemy
from shared import time

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=time.now())
    updated_at = db.Column(db.DateTime, default=time.now(), onupdate=time.now())

