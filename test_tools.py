from datetime import date
from agent.tools import get_order, check_eligibility

order = get_order("ORD-1001")
item_id = order["items"][0]["item_id"]

facts = {"packaging_opened": True}

result = check_eligibility(order, item_id, facts, today=date(2025, 1, 12))
print("Eligibility result:", result)
