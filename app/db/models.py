from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy import *

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    vendor = Column(String, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip = Column(Integer, index=True)
    invoiceNum = Column(Integer)
    invoiceDate = Column()
    invoiceDue = Column()
    invoiceAmountDue = Column()