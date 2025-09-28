from dataclasses import dataclass
from uuid import UUID

@dataclass
class PaymentApproved:
    payment_id: UUID
    buyer_id: UUID
    vehicle_id: UUID

@dataclass
class PaymentRejected:
    payment_id: UUID
    buyer_id: UUID
    vehicle_id: UUID
