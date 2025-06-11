# a fastapi system for account managament

import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    id: int
    name: str
    surname:str

def write_account_to_file(account: Account):
    with open("accounts.txt", "a") as file:
        file.write(f"{account.id}, {account.name}, {account.surname}\n")

def read_accounts_from_file():
    accounts = []
    with open("accounts.txt", "r") as file:
        for line in file:
            id, name, surname = line.strip().split(", ")
            accounts.append(Account(id=int(id), name=name, surname=surname))

    return accounts

def delete_account_from_file(account_id_to_delete: int):
    accounts = read_accounts_from_file()
    accounts = [account for account in accounts if account.id != account_id_to_delete]
    
    with open("accounts.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.id}, {account.name}, {account.surname}\n")


if not os.path.exists("accounts.txt"):
        open("accounts.txt", "w").close()
# type hint for a list of accounts
accounts:list[Account] = read_accounts_from_file()

@app.post("/accounts/")
def create_account(account: Account):
    accounts.append(account)
    write_account_to_file(account)
    return {"message": "Account created successfully"}

@app.get("/accounts/")
def get_accounts():
    return accounts

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    for account in accounts:
        if account.id == account_id:
            return account
    return {"message": "Account not found"}

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    accounts[:] = [account for account in accounts if account.id != account_id]
    delete_account_from_file(account_id)
    return {"message": "Account deleted successfully"}

