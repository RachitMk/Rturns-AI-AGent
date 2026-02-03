from typing import Dict

def normalize_facts(facts: Dict) -> Dict:
    """
    Fix obvious inconsistencies from the LLM output so downstream logic is stable.
    """
    facts = dict(facts)  # copy

    # If packaging is opened, condition should not be "unopened"
    if facts.get("packaging_opened") is True and facts.get("condition") == "unopened":
        facts["condition"] = "opened"

    # If damaged on arrival, condition should be damaged
    if facts.get("damage_on_arrival") is True:
        facts["condition"] = "damaged"

    return facts
