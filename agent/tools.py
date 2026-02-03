from typing import Dict, Any, Optional
from datetime import date

from .utils import load_json, parse_date, days_between

_ORDERS = None
_POLICIES = None

def _load_orders():
    global _ORDERS
    if _ORDERS is None:
        _ORDERS = load_json("orders.json")
    return _ORDERS

def _load_policies():
    global _POLICIES
    if _POLICIES is None:
        _POLICIES = load_json("policies.json")
    return _POLICIES

def get_order(order_id: str) -> Dict[str, Any]:
    for order in _load_orders():
        if order["order_id"] == order_id:
            return order
    raise ValueError(f"Order not found: {order_id}")

def compute_days_since_delivery(order: Dict[str, Any], today: Optional[date] = None) -> int:
    if today is None:
        today = date.today()
    return days_between(parse_date(order["delivery_date"]), today)

def check_eligibility(
    order: Dict[str, Any],
    item_id: str,
    extracted_facts: Dict[str, Any],
    today: Optional[date] = None
) -> Dict[str, Any]:

    if today is None:
        today = date.today()

    item = next((i for i in order["items"] if i["item_id"] == item_id), None)
    if not item:
        raise ValueError("Item not found")

    category = item["category"]
    days_since_delivery = compute_days_since_delivery(order, today)

    if item.get("final_sale") or category == "final_sale":
        return {
            "eligible": False,
            "reason": "final_sale",
            "days_since_delivery": days_since_delivery,
            "allowed_outcomes": ["deny"]
        }

    policy = _load_policies()[category]

    if days_since_delivery > policy["return_window_days"]:
        return {
            "eligible": False,
            "reason": "return_window_exceeded",
            "days_since_delivery": days_since_delivery,
            "allowed_outcomes": ["deny"]
        }

    if extracted_facts.get("packaging_opened") and not policy.get("allow_opened"):
        return {
            "eligible": False,
            "reason": "opened_not_allowed",
            "days_since_delivery": days_since_delivery,
            "allowed_outcomes": ["manual_review"]
        }

    return {
        "eligible": True,
        "reason": "eligible",
        "days_since_delivery": days_since_delivery,
        "allowed_outcomes": policy["allowed_outcomes"]
    }
