from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.ports.repositories import PaymentRepository
from src.domain.models import Payment, PaymentStatus
from src.adapters.db.models import PaymentORM

def _to_domain(row: PaymentORM) -> Payment:
    from uuid import UUID as _UUID
    return Payment(
        id=_UUID(row.id),
        buyer_id=_UUID(row.buyer_id),
        vehicle_id=_UUID(row.vehicle_id),
        amount=row.amount,
        status=PaymentStatus[row.status.name],
        created_at=row.created_at,
        updated_at=row.updated_at,
    )

class SqlAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, payment: Payment) -> Payment:
        row = PaymentORM(
            id=str(payment.id),
            buyer_id=str(payment.buyer_id),
            vehicle_id=str(payment.vehicle_id),
            amount=payment.amount,
            status=payment.status,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return _to_domain(row)

    def get(self, payment_id: UUID) -> Optional[Payment]:
        row = self.db.get(PaymentORM, str(payment_id))
        return _to_domain(row) if row else None

    def list(self, status: Optional[PaymentStatus] = None) -> List[Payment]:
        stmt = select(PaymentORM)
        if status:
            stmt = stmt.where(PaymentORM.status == status)
        rows = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in rows]

    def update_status(self, payment_id: UUID, status: PaymentStatus) -> Payment:
        stmt = (
            update(PaymentORM)
            .where(PaymentORM.id == str(payment_id))
            .values(status=status, updated_at=datetime.utcnow())
            .returning(PaymentORM)
        )
        row = self.db.execute(stmt).fetchone()
        if not row:
            raise LookupError("payment_not_found")
        self.db.commit()
        return _to_domain(row[0])
