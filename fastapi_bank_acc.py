# a fastapi system for Bank accounts and Payment resources creating/management
# check Python version: must be 3.11.9
# to run this code, use command 'fastapi dev fastapi_bank_acc.py'

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from datetime import date

app = FastAPI()

def to_lowercase(s: str) -> str:
    return s.lower()

class BankAccount(BaseModel):
    id: int
    type: Literal["business", "personal"]
    person_name: str
    address: str

    class Config:
        alias_generator = to_lowercase
        populate_by_name = True

bank_accounts: list[BankAccount] = []

@app.post("/bank-accounts/")
def create_bank_account(account: BankAccount):
    bank_accounts.append(account)
    return {"message": "Bank account created successfully"}

@app.get("/bank-accounts/")
def get_bank_accounts():
    return bank_accounts

@app.get("/bank-accounts/{account_id}")
def get_bank_account(account_id: int):
    for account in bank_accounts:
        if account.id == account_id:
            return account
    return {"message": "Such bank account was not found"}

@app.delete("/bank-accounts/{account_id}")
def delete_bank_account(account_id: int):
    bank_accounts[:] = [account for account in bank_accounts if account.id != account_id]
    return {"message": "Bank account deleted successfully"}

class PaymentResource(BaseModel):
    id: str
    from_account_id: int
    to_account_id: int
    amount_in_euros: int
    payment_date: date

class Config:
        alias_generator = to_lowercase
        populate_by_name = True

payment_resources: list[PaymentResource] = []

@app.post("/payment-resources/")
def create_payment_resource(resource: PaymentResource):
    payment_resources.append(resource)
    return {"message": "Payment resource created successfully"}

@app.get("/payment-resources/")
def get_payment_resources():
    return payment_resources

@app.get("/payment-resources/{resource_id}")
def get_payment_resource(resource_id: str):
    for resource in payment_resources:
        if resource.id == resource_id:
            return resource
    return {"message": "Such payment resource was not found"}