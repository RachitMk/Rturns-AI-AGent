from agent.ai_classifier import classify_return
from agent.normalize import normalize_facts

text = "The shoes don't fit. I opened the box but only tried them once."

facts = classify_return(text)
facts = normalize_facts(facts)

print("Extracted facts:", facts)
