from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core import Intake, InvoiceInput

app = FastAPI(title="Invoice intake and local archive")


@lru_cache
def service():
    return Intake()


class Approval(BaseModel):
    fingerprint: str
    reviewer: str
    confirmed: bool = False


@app.post("/api/intake")
def intake(b: InvoiceInput):
    try:
        return service().receive(b.model_dump())
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.post("/api/review/{rid}")
def review(rid: str, b: Approval):
    try:
        return service().approve(rid, **b.model_dump())
    except PermissionError as e:
        raise HTTPException(403, str(e)) from e
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.get("/api/records")
def records():
    return service().records()


@app.get("/api/archive")
def archive():
    return service().archive()
