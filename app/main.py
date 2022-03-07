from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from .database import get_db, engine
from .db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
Get all invoice ids with vendor names
'''
@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "All invoices with vendor names"}

'''
Get specific invoice by vendor name
'''
@app.get("/{vendor_name}")
async def get_vendor_invoice(vendor_name: str, db: Session = Depends(get_db)):
    
    return {"message": "Vendor Invoice",
            "vendor": vendor_name} 

'''
Get invoice data by unique identifier
'''
@app.get("/invoices/{submissionID}")
async def get_invoice(submissionID: int, db: Session = Depends(get_db)):
    return {"message": "Vendor Invoice With Information",
            "submissionID": submissionID} 
 
