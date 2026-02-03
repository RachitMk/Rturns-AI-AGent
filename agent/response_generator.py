from typing import Dict


def generate_customer_message(facts: Dict, decision: Dict) -> str:
    """
    Create a customer-facing message explaining the outcome.
    """

    # ---------- NOT ELIGIBLE CASES ----------
    if not decision["eligible"]:

        if decision["reason"] == "damaged_on_arrival":
            return (
                "Thanks for letting us know. Since the item arrived damaged, "
                "we’ve approved your return and our team will assist you with the next steps."
            )

        if decision["reason"] == "late_delivery":
            return (
                "We’re sorry about the delayed delivery. As a courtesy, "
                "we’re offering compensation for this order."
            )

        if decision["reason"] == "return_window_exceeded":
            return (
                "Thanks for reaching out. Unfortunately, your return request "
                "is outside our return window, so we’re unable to process it."
            )

        if decision["reason"] == "final_sale":
            return (
                "Thanks for contacting us. This item was marked as final sale, "
                "so it isn’t eligible for return."
            )

        return (
            "Thanks for your request. We’re unable to process this return "
            "based on our return policy."
        )

    # ---------- ELIGIBLE CASES ----------
    outcomes = decision.get("allowed_outcomes", [])

    if "refund" in outcomes and "exchange" in outcomes:
        return (
            "Your return request has been approved. Since the item was returned "
            "within the eligible window, you may choose between a refund or an exchange."
        )

    if "exchange" in outcomes:
        return (
            "Your return request has been approved. You’re eligible for an exchange. "
            "Please select a replacement item to continue."
        )

    if "store_credit" in outcomes:
        return (
            "Your request has been reviewed, and we’re happy to offer store credit "
            "for this return."
        )

    return "Your return request has been approved."


def generate_ops_notes(
    facts: Dict, decision: Dict, confidence: float, routing: str
) -> str:
    """
    Create internal notes explaining how the decision was reached.
    """
    lines = [
        f"Return category: {facts.get('return_category')}",
        f"Condition: {facts.get('condition')}",
        f"Packaging opened: {facts.get('packaging_opened')}",
        f"Days since delivery: {decision.get('days_since_delivery')}",
        f"Decision reason: {decision.get('reason')}",
        f"Allowed outcomes: {decision.get('allowed_outcomes')}",
        f"Confidence: {confidence:.2f}",
        f"Routing: {routing}",
    ]
    return "\n".join(lines)


def compute_confidence(facts: Dict, decision: Dict) -> float:
    """
    Simple confidence heuristic.
    """
    confidence = 0.6

    if decision["eligible"]:
        confidence += 0.2

    if facts.get("return_category") in ["size_issue", "damaged_item"]:
        confidence += 0.1

    if facts.get("damage_on_arrival"):
        confidence += 0.1

    return min(confidence, 0.95)
