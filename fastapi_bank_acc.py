# a fastapi system for Bank accounts and Payment resources creating/management
# information about bank accounts and payment resources is stored in database files .txt
# check Python version: must be 3.11.9
# to run this code, use command 'fastapi dev fastapi_bank_acc.py'

import os
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

def write_account_to_file(account: BankAccount):
    with open("accounts_database.txt", "a") as file:
        file.write(f"{account.id}, {account.type}, {account.person_name}, {account.address}\n")

def read_accounts_from_file():
    accounts = []
    with open("accounts_database.txt", "r") as file:
        for line in file:
            id, type_str, person_name, address = line.strip().split(", ")
            type_literal = type_str if type_str in ("business", "personal") else "personal"
            accounts.append(BankAccount(id=int(id), type=type_literal, person_name=person_name, address=address))

    return accounts

def delete_account_from_file(account_id_to_delete: int):
    accounts = read_accounts_from_file()
    accounts = [account for account in accounts if account.id != account_id_to_delete]
    
    with open("accounts_database.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.address}\n")

if not os.path.exists("accounts_database.txt"):
        open("accounts_database.txt", "w").close()

# type hint for a list of accounts
accounts:list[BankAccount] = read_accounts_from_file()

bank_accounts: list[BankAccount] = []

@app.post("/bank-accounts/")
def create_bank_account(account: BankAccount):
    bank_accounts.append(account)
    write_account_to_file(account)
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

def write_payment_to_file(payment: PaymentResource):
    with open("payments_database.txt", "a") as file:
        file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount_in_euros}, {payment.payment_date}\n")

def read_payments_from_file():
    payments = []
    with open("payments_database.txt", "r") as file:
        for line in file:
            id, from_account_id, to_account_id, amount_in_euros, payment_date = line.strip().split(", ")
            payments.append(PaymentResource(id=id, from_account_id=int(from_account_id), to_account_id=int(to_account_id), amount_in_euros=int(amount_in_euros), payment_date=date.fromisoformat(payment_date)))

    return payments

def delete_payments_from_file(payment_id_to_delete: str):
    payments = read_payments_from_file()
    payments = [payment for payment in payments if payment.id != payment_id_to_delete]
    
    with open("payments_database.txt", "w") as file:
        for payment in payments:
            file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount_in_euros}, {payment.payment_date}\n")

if not os.path.exists("payments_database.txt"):
        open("payments_database.txt", "w").close()

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