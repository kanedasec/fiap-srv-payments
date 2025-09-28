from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from uuid import UUID

from src.adapters.db.base import SessionLocal, engine
from src.adapters.db.repository import SqlAlchemyPaymentRepository
from src.domain.models import PaymentStatus

router = APIRouter()

def get_repo():
    db = SessionLocal()
    try:
        yield SqlAlchemyPaymentRepository(db)
    finally:
        db.close()

class HealthResponse(BaseModel):
    status: str

@router.get("/healthz", response_model=HealthResponse, tags=["health"])
def healthz():
    return {"status": "ok"}

@router.get("/readyz", response_model=HealthResponse, tags=["health"])
def readyz():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        return {"status": "degraded"}

# ---- Schemas
class PaymentIn(BaseModel):
    buyer_id: UUID
    vehicle_id: UUID
    amount: float = Field(gt=0)

class PaymentOut(BaseModel):
    id: UUID
    buyer_id: UUID
    vehicle_id: UUID
    amount: float
    status: PaymentStatus

class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus

# ---- Endpoints
from src.application.usecases.create_payment import create_payment
from src.application.usecases.update_payment import update_payment_status
from src.application.usecases.list_payments import list_payments

@router.post("/payments", response_model=PaymentOut, tags=["payments"])
def create_payment_endpoint(data: PaymentIn, repo: SqlAlchemyPaymentRepository = Depends(get_repo)):
    p = create_payment(repo, data.model_dump())
    return jsonable_encoder(p)

@router.get("/payments", response_model=list[PaymentOut], tags=["payments"])
def list_payments_endpoint(status: PaymentStatus | None = None, repo: SqlAlchemyPaymentRepository = Depends(get_repo)):
    items = list_payments(repo, status)
    return jsonable_encoder(items)

@router.get("/payments/{payment_id}", response_model=PaymentOut, tags=["payments"])
def get_payment(payment_id: UUID, repo: SqlAlchemyPaymentRepository = Depends(get_repo)):
    p = repo.get(payment_id)
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")
    return jsonable_encoder(p)

@router.patch("/payments/{payment_id}", response_model=PaymentOut, tags=["payments"])
def update_payment_endpoint(payment_id: UUID, body: PaymentStatusUpdate, repo: SqlAlchemyPaymentRepository = Depends(get_repo)):
    try:
        p = update_payment_status(repo, payment_id, body.status)
        return jsonable_encoder(p)
    except LookupError:
        raise HTTPException(status_code=404, detail="Payment not found")
