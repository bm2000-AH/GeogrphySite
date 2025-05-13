import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Tabls(SqlAlchemyBase, UserMixin):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    strana = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)

    user = orm.relationship('User')