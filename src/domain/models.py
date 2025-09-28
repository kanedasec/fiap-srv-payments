from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

@dataclass
class Payment:
    buyer_id: UUID
    vehicle_id: UUID
    amount: float

    id: UUID = field(default_factory=uuid4)
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


    @staticmethod
    def new(buyer_id: UUID, vehicle_id: UUID, amount: float) -> "Payment":
        now = datetime.utcnow()
        return Payment(
            id=uuid4(),
            buyer_id=buyer_id,
            vehicle_id=vehicle_id,
            amount=amount,
            status=PaymentStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
