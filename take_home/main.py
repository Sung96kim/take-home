import aiofiles
import os
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile
from fastapi.responses import HTMLResponse
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

from .schemas import GetSingleInvoice, PostInvoice, GetInvoices

my_config = IndicoConfig(host="app.indico.io", api_token_path="./indico_api_token.txt")
client = IndicoClient(config=my_config)

workflow_id = 933
directory = "/home/sung96kim/take-home/temp_folder"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def main():
    content = """
        <body>
            <form action="/invoices/uploadfiles" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)


"""
Get all invoice ids with vendor names
"""


@app.get("/invoices")
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


@app.get("/invoices/{vendor_name}")
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


@app.get("/invoice/{submissionID}")
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


@app.post("/invoices/uploadfiles", status_code=status.HTTP_201_CREATED)
async def post_invoice(
    files: List[UploadFile],
    db: Session = Depends(get_db),
):
    try:
        fileList = []

        for file in files:
            async with aiofiles.open(f"{directory}/{file.filename}", "wb") as tmp:
                while True:
                    content = await file.read(1024)
                    if not content:
                        break
                    await tmp.write(content)
            fileList.append(tmp.name)

        submission_ids = client.call(
            WorkflowSubmission(
                workflow_id=workflow_id,
                files=fileList,
            )
        )

        submissionList = []

        for submission_id in submission_ids:
            result_url = client.call(SubmissionResult(submission_id, wait=True))
            result = client.call(RetrieveStorageObject(result_url.result))["results"][
                "document"
            ]["results"]["Invoice Fields q2026 model"]["final"]

            submissionObj = {}
            for cols in result:
                submissionObj[cols["label"]] = cols["text"]
                if submissionObj[cols["label"]] == "Invoice #":
                    submissionObj[cols["label"]] == "".join(
                        filter(str.isdigit), cols["text"]
                    )

            template: PostInvoice = {
                "vendor": submissionObj.get("Vendor Name"),
                "street": submissionObj.get("Vendor Street"),
                "city": submissionObj.get("Vendor City"),
                "state": submissionObj.get("Vendor State"),
                "zip": submissionObj.get("Vendor Zip"),
                "invoiceNum": submissionObj.get("Invoice #"),
                "invoiceDate": submissionObj.get("Invoice Date"),
                "invoiceDue": submissionObj.get("Due Date"),
                "invoiceAmountDue": submissionObj.get("Amount Due"),
            }

            submissionList.append(template)
            client.call(UpdateSubmission(submission_id, retrieved=True))

        # For each submission, add into database
        for submission in submissionList:
            invoice = Invoice(**submission)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)

        # Remove created temp files after checking if they exist
        for tempFile in fileList:
            if os.path.exists(tempFile):
                os.remove(tempFile)

        return submissionList

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There was a problem with adding the invoice(s) to the database",
        )
