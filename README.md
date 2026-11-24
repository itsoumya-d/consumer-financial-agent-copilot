# consumer-financial-agent-copilot

Autonomous consumer financial copilot, transaction classification engine, recurring subscription creep detector, and personal cashflow optimizer in Python.

## Overview
Consumer fintech platforms serving millions of users require intelligent, deterministic client-side and backend financial reasoning:
- **Transaction Categorization**: Classifies raw bank/merchant transaction strings into deterministic spending taxonomies (groceries, utilities, entertainment, recurring subscriptions).
- **Subscription Creep Detector**: Analyzes transaction cadences and merchant intervals to isolate recurring subscription renewals and price increases.
- **Cashflow Velocity & Savings Advisor**: Computes monthly burn rate, discretionary spending headroom, and generates personalized savings targets.
- **Tool-Calling Agent Interface**: Structured prompt and tool-execution contracts compatible with frontier LLMs (Claude 3.5 Sonnet) for natural-language financial queries with schema-validated outputs.

## Installation & Testing
```bash
pip install -r requirements.txt
pytest -v
```
