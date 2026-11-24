from src.fin_agent.engine import FinancialCopilotEngine
from src.fin_agent.models import Transaction, TransactionCategory


def test_transaction_categorization():
    copilot = FinancialCopilotEngine()
    assert copilot.categorize_transaction("Payroll Direct Deposit", -3500.0) == TransactionCategory.INCOME
    assert copilot.categorize_transaction("Whole Foods Market", 124.50) == TransactionCategory.GROCERIES
    assert copilot.categorize_transaction("Netflix Subscription", 19.99) == TransactionCategory.SUBSCRIPTIONS
    assert copilot.categorize_transaction("Uber Trip", 24.10) == TransactionCategory.TRANSPORT
    assert copilot.categorize_transaction("Chipotle Mexican Grill", 14.50) == TransactionCategory.DINING


def test_subscription_detection_and_creep():
    copilot = FinancialCopilotEngine()
    txs = [
        Transaction("1", "2026-09-01", "Netflix", 15.99),
        Transaction("2", "2026-10-01", "Netflix", 17.99),
        Transaction("3", "2026-11-01", "Netflix", 19.99),
        Transaction("4", "2026-11-05", "Trader Joe's", 85.00),
    ]
    subs = copilot.detect_subscriptions(txs)
    assert len(subs) == 1
    assert subs[0].merchant == "Netflix"
    assert subs[0].detected_increase is True


def test_cashflow_summary_computation():
    copilot = FinancialCopilotEngine()
    txs = [
        Transaction("1", "2026-11-01", "Payroll", -5000.0),
        Transaction("2", "2026-11-02", "Whole Foods", 200.0),
        Transaction("3", "2026-11-03", "Electric Utility", 150.0),
        Transaction("4", "2026-11-04", "Spotify", 12.99),
        Transaction("5", "2026-10-04", "Spotify", 12.99),
    ]
    summary = copilot.compute_cashflow_summary(txs)
    assert summary.total_income == 5000.0
    assert summary.total_expenses == 375.98
    assert summary.net_savings == 4624.02
    assert summary.savings_rate_pct > 90.0
    assert len(summary.subscriptions) == 1


def test_claude_tool_definition():
    copilot = FinancialCopilotEngine()
    tool = copilot.build_tool_definition()
    assert tool["name"] == "analyze_consumer_finances"
    assert "input_schema" in tool
    assert tool["input_schema"]["type"] == "object"
