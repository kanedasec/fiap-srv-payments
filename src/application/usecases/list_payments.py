from typing import Optional, List
from src.ports.repositories import PaymentRepository
from src.domain.models import Payment, PaymentStatus

def list_payments(repo: PaymentRepository, status: Optional[PaymentStatus] = None) -> List[Payment]:
    return repo.list(status)
