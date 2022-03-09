import shutil
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    # files: List[UploadFile] = File(...),
    # template: PostInvoice,
    db: Session = Depends(get_db),
):
    # copiedFiles = []
    # for file in files:
    #     with open(file.filename, "r+b") as buffer:
    #         copiedFiles.append(await buffer.read())

    # submission_ids = client.call(
    #     WorkflowSubmission(
    #         workflow_id=workflow_id,
    #         files=copiedFiles,
    #     )
    # )
    # submission_id = submission_ids[0]

    # result_url = client.call(SubmissionResult(submission_id, wait=True))
    # result = client.call(RetrieveStorageObject(result_url.result))

    # client.call(UpdateSubmission(submission_id, retrieved=True))

    # return result

    # finally:
    #     return {"Uploaded Files" : [file.filename for file in files]}

    # try:
    submission_ids = client.call(
        WorkflowSubmission(
            workflow_id=workflow_id,
            files=[
                "./assets/AriatInvoice03.28.19.pdf",
                # "./assets/ERS Invoice 03.19.19 (3)_2.pdf",
                # "./assets/ERS Invoice 06.05.18 .pdf",
                # "./assets/ERS Invoice 12.26.19 .pdf",
                # "./assets/ERSInvoice01.02.18_2.pdf",
                "./assets/Kerrits Invoice 10.15.19.pdf",
                # "./assets/Kerrits Invoice 10.22.19 (2).pdf",
                "./assets/RJ Matthews Invoice 01.21.19 (1).pdf",
                "./assets/RJ Matthews Invoice 01.28.19 .pdf",
                "./assets/RJ Matthews Order 01.21.19 (2).pdf",
                "./assets/RJ Matthews Order 01.23.19 .pdf",
                "./assets/RJ Matthews Order 02.11.19 .pdf",
                "./assets/RJ Matthews Order 03.11.19 .pdf",
                "./assets/RJ Matthews Order 03.27.19 .pdf",
                "./assets/RJ Matthews Order 05.06.19.pdf",
            ],
        )
    )

    submissionID = submission_ids[0]
    submissionList = list()

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
        client.call(UpdateSubmission(submissionID, retrieved=True))

    for submission in submissionList:
        invoice = Invoice(**submission)
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

    return submissionList


# except:
#     raise HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail=f"There was a problem with adding the invoice(s) to the database",
#     )
