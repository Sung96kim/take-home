from datetime import datetime
from pydantic import BaseModel


class PostInvoice(BaseModel):
    vendor: str
    street: str
    city: str
    state: str
    zip: int
    invoiceNum: int
    invoiceDate: str
    invoiceDue: str
    invoiceAmountDue: str
    created_at: datetime


class GetInvoices(BaseModel):
    id: int
    vendor: str


class GetSingleInvoice(PostInvoice):
    id: int
