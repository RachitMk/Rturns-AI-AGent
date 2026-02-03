# Returns Processing AI Agent

This project is an AI-powered returns processing agent that classifies customer return requests,
applies deterministic retail policies, and decides whether a return can be automated or requires
human review.

## 🚀 Key Features
- Natural language understanding of customer return requests
- Deterministic policy enforcement (return windows, categories, conditions)
- Confidence scoring to assess decision certainty
- Human-in-the-loop routing for ambiguous or high-risk cases
- Streamlit-based interactive UI for demo and testing

## 🧠 How the Agent Works
1. AI extracts structured facts from unstructured customer messages
2. Business rules determine eligibility and allowed outcomes
3. Confidence score evaluates clarity and risk
4. Agent decides whether to auto-process or route to manual review

## 🛠 Tech Stack
- Python
- Streamlit
- Groq LLM API
- Rule-based policy engine

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
