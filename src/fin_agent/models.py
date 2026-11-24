from dataclasses import dataclass, field
from enum import Enum


class TransactionCategory(str, Enum):
    INCOME = "INCOME"
    GROCERIES = "GROCERIES"
    UTILITIES = "UTILITIES"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"
    DINING = "DINING"
    TRANSPORT = "TRANSPORT"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"


@dataclass
class Transaction:
    id: str
    date: str
    merchant: str
    amount: float
    category: TransactionCategory = TransactionCategory.OTHER


@dataclass
class SubscriptionInsight:
    merchant: str
    monthly_cost: float
    cadence_days: int
    detected_increase: bool = False
    confidence: float = 1.0


@dataclass
class CashflowSummary:
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate_pct: float
    subscriptions: list[SubscriptionInsight] = field(default_factory=list)
