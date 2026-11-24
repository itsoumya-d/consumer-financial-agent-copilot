from typing import Any
from .models import CashflowSummary, SubscriptionInsight, Transaction, TransactionCategory


class FinancialCopilotEngine:
    """Consumer financial planning, transaction intelligence, and budgeting copilot."""

    CATEGORY_PATTERNS = {
        TransactionCategory.SUBSCRIPTIONS: {"netflix", "spotify", "apple.com/bill", "hulu", "prime", "gym", "sub"},
        TransactionCategory.GROCERIES: {"trader joe", "whole foods", "safeway", "supermarket", "walmart", "costco"},
        TransactionCategory.DINING: {"uber eats", "doordash", "chipotle", "starbucks", "restaurant", "cafe"},
        TransactionCategory.TRANSPORT: {"uber", "lyft", "metro", "transit", "chevron", "shell"},
        TransactionCategory.UTILITIES: {"electric", "water", "internet", "comcast", "att", "verizon"},
    }

    def categorize_transaction(self, merchant: str, amount: float) -> TransactionCategory:
        """Categorize raw merchant transactions into deterministic financial spending buckets."""
        if amount < 0:
            return TransactionCategory.INCOME

        low = merchant.lower()
        for cat, patterns in self.CATEGORY_PATTERNS.items():
            if any(p in low for p in patterns):
                return cat

        return TransactionCategory.OTHER

    def detect_subscriptions(self, transactions: list[Transaction]) -> list[SubscriptionInsight]:
        """Detect recurring transaction cadences and potential subscription creep."""
        merchant_txs: dict[str, list[Transaction]] = {}
        for tx in transactions:
            if tx.amount <= 0:
                continue
            norm = tx.merchant.strip().lower()
            merchant_txs.setdefault(norm, []).append(tx)

        subscriptions = []
        for merchant, txs in merchant_txs.items():
            if len(txs) >= 2:
                # Sort by date
                sorted_txs = sorted(txs, key=lambda t: t.date)
                amounts = [t.amount for t in sorted_txs]
                avg_cost = sum(amounts) / len(amounts)
                has_increase = amounts[-1] > amounts[0]

                subscriptions.append(
                    SubscriptionInsight(
                        merchant=merchant.title(),
                        monthly_cost=round(avg_cost, 2),
                        cadence_days=30,
                        detected_increase=has_increase,
                        confidence=0.95,
                    )
                )

        return sorted(subscriptions, key=lambda s: s.monthly_cost, reverse=True)

    def compute_cashflow_summary(self, transactions: list[Transaction]) -> CashflowSummary:
        """Compute aggregated monthly cashflow and personal savings rate."""
        income = sum(abs(t.amount) for t in transactions if t.amount < 0)
        expenses = sum(t.amount for t in transactions if t.amount > 0)
        net_savings = income - expenses
        savings_rate = (net_savings / income * 100) if income > 0 else 0.0

        subscriptions = self.detect_subscriptions(transactions)

        return CashflowSummary(
            total_income=round(income, 2),
            total_expenses=round(expenses, 2),
            net_savings=round(net_savings, 2),
            savings_rate_pct=round(savings_rate, 1),
            subscriptions=subscriptions,
        )

    def build_tool_definition(self) -> dict[str, Any]:
        """Generate structured tool-calling definition compatible with the Claude API."""
        return {
            "name": "analyze_consumer_finances",
            "description": "Analyzes raw bank transactions, categorizes expenses, and identifies subscription creep.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "transactions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "date": {"type": "string"},
                                "merchant": {"type": "string"},
                                "amount": {"type": "number"},
                            },
                            "required": ["id", "date", "merchant", "amount"],
                        },
                    }
                },
                "required": ["transactions"],
            },
        }
