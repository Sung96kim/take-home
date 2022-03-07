from email.policy import HTTP
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from indico import IndicoClient, IndicoConfig
from indico.queries import (
    RetrieveStorageObject,
    SubmissionResult,
    UpdateSubmission,
    WorkflowSubmission,
)

from .database import get_db, engine
from .db import models, Invoice
from schemas import GetSingleInvoice, PostInvoice, GetInvoices

my_config = IndicoConfig(host="app.indico.io", api_token_path="./indico_api_token.txt")
client = IndicoClient(config=my_config)

workflow_id = 933

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
Get all invoice ids with vendor names
"""


@app.get("/invoices", response_model=List[GetInvoices])
async def root(db: Session = Depends(get_db)):

    all_invoices = db.query(Invoice).all()

    if not all_invoices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No invoices found"
        )

    return all_invoices


"""
Get specific invoice by vendor name
"""


@app.get("/invoices/{vendor_name}", response_model=List[GetSingleInvoice])
async def get_vendor_invoices(vendor_name: str, db: Session = Depends(get_db)):

    vendor_invoices = db.query(Invoice).filter(Invoice.vendor == vendor_name).all()

    if not vendor_invoices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendor name does not exist in database",
        )

    return vendor_invoices


"""
Get invoice data by unique identifier
"""


@app.get("/invoice/{submissionID}", response_model=GetSingleInvoice)
async def get_invoice(submissionID: int, db: Session = Depends(get_db)):

    invoice = db.query(Invoice).filter(Invoice.id == submissionID).first()

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice by that ID does not exist",
        )

    return invoice


"""
Post invoice
"""


@app.post("/")
async def post_invoice(post: PostInvoice, db: Session = Depends(get_db)):

    submission_ids = client.call(
        WorkflowSubmission(
            workflow_id=workflow_id, files=["./assets/AriatInvoice03.28.19.pdf"]
        )
    )
    submission_id = submission_ids[0]

    result_url = client.call(SubmissionResult(submission_id, wait=True))
    result = client.call(RetrieveStorageObject(result_url.result))["results"][
        "document"
    ]["results"]["Invoice Fields q2026 model"]["final"]

    client.call(UpdateSubmission(submission_id, retrieved=True))

    return
