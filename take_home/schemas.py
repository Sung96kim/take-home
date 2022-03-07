from datetime import datetime
from numpy import integer
from pydantic import BaseModel


class PostInvoice(BaseModel):
    vendor: str
    street: str
    city: str
    state: str
    zip: str
    invoiceNum: str
    invoiceDate: str
    invoiceDue: str
    invoiceAmountDue: str
    created_at: datetime


class GetInvoices(BaseModel):
    id: integer
    vendor: str


class GetSingleInvoice(PostInvoice):
    pass
