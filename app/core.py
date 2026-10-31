import hashlib
import json
import tempfile
import uuid
from pathlib import Path
from pydantic import BaseModel, Field
from sqlalchemy import String, select, update
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base, database


class InvoiceInput(BaseModel):
    number: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    subtotal_cents: int = Field(ge=0, strict=True)
    tax_cents: int = Field(ge=0, strict=True)
    total_cents: int = Field(ge=0, strict=True)


class Record(Base):
    __tablename__ = "invoice_intake"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    invoice_key: Mapped[str] = mapped_column(unique=True)
    body: Mapped[str]
    fingerprint: Mapped[str]
    status: Mapped[str]
    issues: Mapped[str]
    reviewer: Mapped[str | None]


class Archive(Base):
    __tablename__ = "archive"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    body: Mapped[str]


class Intake:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)

    def receive(self, item):
        item = InvoiceInput.model_validate(item)
        body = item.model_dump_json()
        key = item.vendor + "::" + item.number
        with self.sessions.begin() as s:
            old = s.scalar(select(Record).where(Record.invoice_key == key))
            if old:
                if old.body != body:
                    raise ValueError("invoice number reused with different content")
                return self.view(old)
            issues = [] if item.subtotal_cents + item.tax_cents == item.total_cents else ["total mismatch"]
            r = Record(
                id=str(uuid.uuid4()),
                invoice_key=key,
                body=body,
                fingerprint=hashlib.sha256(body.encode()).hexdigest(),
                status="needs_correction" if issues else "pending_review",
                issues=json.dumps(issues),
                reviewer=None,
            )
            s.add(r)
            return self.view(r)

    @staticmethod
    def view(r):
        return dict(
            id=r.id,
            invoice=json.loads(r.body),
            fingerprint=r.fingerprint,
            status=r.status,
            issues=json.loads(r.issues),
            reviewer=r.reviewer,
        )

    def approve(self, rid, fingerprint, reviewer, confirmed=False):
        if not confirmed or not reviewer.strip():
            raise PermissionError("explicit identified human approval required")
        with self.sessions.begin() as s:
            r = s.get(Record, rid)
            if not r or r.fingerprint != fingerprint:
                raise ValueError("unknown or changed invoice")
            if r.status == "archived":
                return self.view(r)
            result = s.execute(
                update(Record)
                .where(Record.id == rid, Record.status == "pending_review")
                .values(status="archived", reviewer=reviewer)
            )
            if result.rowcount != 1:
                raise ValueError("invoice requires correction")
            s.add(Archive(id=rid, body=r.body))
            s.refresh(r)
            return self.view(r)

    def records(self):
        with self.sessions() as s:
            return [self.view(r) for r in s.scalars(select(Record))]

    def archive(self):
        with self.sessions() as s:
            return [json.loads(r.body) for r in s.scalars(select(Archive))]


SAMPLE = dict(number="DEMO-42", vendor="Example Ltd", subtotal_cents=10000, tax_cents=2100, total_cents=12100)


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        s = Intake("sqlite:///" + str(Path(d) / "invoices.sqlite"))
        a = s.receive(SAMPLE)
        b = s.receive(SAMPLE)
        s.approve(a["id"], a["fingerprint"], "Demo reviewer", True)
        bad = s.receive(dict(SAMPLE, number="DEMO-43", total_cents=99999))
        return dict(duplicate_same_id=a["id"] == b["id"], bad=bad, archive=s.archive())


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(
        passed=r["duplicate_same_id"] and len(r["archive"]) == 1 and r["bad"]["status"] == "needs_correction",
        scenario=r,
    )
