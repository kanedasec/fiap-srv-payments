from uuid import UUID
from src.ports.repositories import PaymentRepository
from src.domain.models import Payment

def create_payment(repo: PaymentRepository, data: dict) -> Payment:
    from datetime import datetime
    from uuid import uuid4

    payment = Payment(
        id=uuid4(),
        buyer_id=data["buyer_id"],
        vehicle_id=data["vehicle_id"],
        amount=data["amount"],
        status="PENDING",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return repo.add(payment)
