# a fastapi system for Bank Account creating and management
# check Python version: must be 3.11.9
# to run this code, use command 'fastapi dev fastapi_bank_acc.py'

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()
class BankAccount(BaseModel):
    id: int
    type: Literal["business", "personal"]
    person_name: str
    address: str

# type hint for a list of BankAccounts

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
