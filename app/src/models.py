# models.py

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "payments"
    # __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    amount = Column(Float)
    payer = Column(String)
    split_with = Column(String)

    def __repr__(self):
        return (f"<Expense(id={self.id}, description='{self.description}', amount={self.amount}, "
                f"payer='{self.payer}', split_with='{self.split_with}')>")