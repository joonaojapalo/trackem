from app import app
from flask.ext.sqlalchemy import SQLAlchemy

#define db
db = SQLAlchemy()
db.init_app(app)

__all__ = ["db"]

