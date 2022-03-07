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


class GetInvoices(BaseModel):
    id: integer
    vendor: str
