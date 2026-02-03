from datetime import date
from agent.ai_classifier import classify_return
from agent.normalize import normalize_facts
from agent.tools import get_order, check_eligibility
from agent.response_generator import (
    generate_customer_message,
    generate_ops_notes,
    compute_confidence
)

order = get_order("ORD-1001")
item_id = order["items"][0]["item_id"]

text = "The shoes don't fit. I opened the box but only tried them once."

facts = normalize_facts(classify_return(text))

decision = check_eligibility(
    order,
    item_id,
    facts,
    today=date(2025, 1, 12)
)

customer_message = generate_customer_message(facts, decision)
ops_notes = generate_ops_notes(facts, decision)
confidence = compute_confidence(facts, decision)

print("\n=== AGENT OUTPUT ===")
print("Facts:", facts)
print("Decision:", decision)
print("\nCustomer message:")
print(customer_message)
print("\nOps notes:")
print(ops_notes)
print("\nConfidence score:", confidence)
