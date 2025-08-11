from sqlalchemy import Column, String, Integer, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class Bank(str, enum.Enum):
    sber = "Сбер"
    tbank = "Т-банк"


class Role(int, enum.Enum):
    admin = 1
    user = 2


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True, index=True, nullable=False)
    chat_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    bank = Column(SqlEnum(Bank), nullable=True)
    role = Column(SqlEnum(Role), default=Role.user, nullable=False)


# id = db.Column(db.Integer, primary_key=True)
    # tg_id = db.Column(db.BigInteger, unique=True, nullable=False)
    # username = db.Column(db.String(50))
    # first_name = db.Column(db.String(100))
    # last_name = db.Column(db.String(100))
    # phone = db.Column(db.String(20))
    # # bank = db.Column(db.String(50))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow

# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     description = db.Column(db.String(200))
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


# class EventParticipant(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class Expense(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#     paid_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     title = db.Column(db.String(100))
#     description = db.Column(db.String(200))
#     amount = db.Column(db.Float)

# class ExpenseShare(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     share_amount = db.Column(db.Float)
