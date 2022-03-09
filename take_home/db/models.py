from re import S
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy import *


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    vendor = Column(String, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip = Column(Integer, index=True)
    invoiceNum = Column(Integer)
    invoiceDate = Column(String)
    invoiceDue = Column(String)
    invoiceAmountDue = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
