import streamlit as st
from datetime import date

from agent.ai_classifier import classify_return
from agent.normalize import normalize_facts
from agent.tools import get_order, check_eligibility
from agent.response_generator import (
    generate_customer_message,
    generate_ops_notes,
    compute_confidence
)

st.set_page_config(page_title="Returns Processing AI Agent", layout="centered")

MANUAL_REVIEW_THRESHOLD = 0.75

st.title("🛍️ Returns Processing AI Agent")
st.caption("AI-powered return classification with deterministic policy enforcement")

# --- Inputs ---
order_id = st.text_input("Order ID", value="ORD-1001")
item_index = st.number_input("Item index in order", min_value=0, value=0)
return_text = st.text_area(
    "Customer return request",
    value="The shoes don't fit. I opened the box but only tried them once."
)

process = st.button("Process Return")

# --- Processing ---
if process:
    try:
        order = get_order(order_id)

        # Validate item_index (prevents crashes)
        if item_index >= len(order["items"]):
            st.error(
                f"This order has only {len(order['items'])} item(s). "
                f"Please select an item index between 0 and {len(order['items']) - 1}."
            )
            st.stop()

        item_id = order["items"][item_index]["item_id"]

        with st.spinner("Understanding return request..."):
            facts = normalize_facts(classify_return(return_text))

        decision = check_eligibility(
            order,
            item_id,
            facts,
            today=date(2025, 1, 12)  # freeze date for demo stability
        )

        customer_message = generate_customer_message(facts, decision)

        # Confidence first
        confidence = compute_confidence(facts, decision)

        # Manual review trigger logic
        manual_review_by_policy = "manual_review" in (decision.get("allowed_outcomes") or [])
        manual_review_by_confidence = confidence < MANUAL_REVIEW_THRESHOLD

        needs_manual_review = manual_review_by_policy or manual_review_by_confidence
        routing = "manual_review" if needs_manual_review else "auto_process"

        # Ops notes (include routing + confidence)
        ops_notes = generate_ops_notes(facts, decision, confidence, routing)

        # --- Outputs ---
        st.success("Return processed successfully")

        st.subheader("🔍 Extracted Facts")
        st.json(facts)

        st.subheader("⚖️ Decision")
        st.json(decision)

        st.subheader("💬 Customer Message")
        st.write(customer_message)

        st.subheader("🛠️ Ops Notes")
        st.text(ops_notes)

        st.subheader("📊 Confidence Score")
        st.caption("Confidence reflects how clearly the request matches order data + policies.")
        st.progress(confidence)
        st.write(f"{confidence:.2f}")

        st.subheader("🧑‍💼 Routing")
        if routing == "manual_review":
            st.warning(
                "⚠️ Manual review recommended.\n\n"
                "Reason: "
                + ("Policy requires manual review. " if manual_review_by_policy else "")
                + (f"Low confidence ({confidence:.2f} < {MANUAL_REVIEW_THRESHOLD})." if manual_review_by_confidence else "")
            )
        else:
            st.success("✅ Safe to auto-process (no manual review needed).")

    except Exception as e:
        st.error(f"Error: {str(e)}")
