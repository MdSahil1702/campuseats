from typing import Dict, Optional
from models import Order


class OrderStore:
    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._idempotency: Dict[str, str] = {}
        self._next_internal_id = 1

    def next_id(self) -> int:
        value = self._next_internal_id
        self._next_internal_id += 1
        return value

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def list(self, status: Optional[str] = None):
        values = list(self._orders.values())
        if status:
            values = [o for o in values if o.status == status]
        return values

    def remember_idempotency(self, key: str, order_id: str) -> None:
        self._idempotency[key] = order_id

    def get_idempotent_order(self, key: str) -> Optional[Order]:
        order_id = self._idempotency.get(key)
        return self.get(order_id) if order_id else None
