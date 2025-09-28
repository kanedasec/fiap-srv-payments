from uuid import UUID
from src.ports.repositories import PaymentRepository
from src.domain.models import PaymentStatus, Payment

def update_payment_status(repo: PaymentRepository, payment_id: UUID, new_status: PaymentStatus) -> Payment:
    return repo.update_status(payment_id, new_status)
