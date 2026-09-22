import re
from typing import Dict, Any, Optional


EXPENSE_KEYWORDS = ["spent", "buy", "bought", "paid", "purchase"]
REPORT_KEYWORDS = ["report", "summary", "spending"]
INCOME_KEYWORDS = [
    "salary",
    "bonus",
    "income",
    "paycheck",
    "wage",
    "freelance",
    "commission",
    "refund",
    "cashback",
    "interest",
    "dividend",
    "gift"
]


def detect_intent(text: str) -> str:
    text_lower = text.lower()

    if any(re.search(rf"\b{re.escape(word)}\b", text_lower) for word in EXPENSE_KEYWORDS):
        return "add_expense"

    if any(word in text_lower for word in REPORT_KEYWORDS):
        return "get_report"

    return "unknown"


def extract_amount(text: str) -> Optional[int]:
    match = re.search(r'(\d[\d.,]*)', text)
    if not match:
        return None

    raw_amount = match.group(1)
    clean_amount = re.sub(r"[^\d]", "", raw_amount)

    return int(clean_amount) if clean_amount else None


def detect_report_period(text: str) -> str | None:
    text_lower = text.lower()

    if "daily" in text_lower or "today" in text_lower:
        return "daily"
    if "weekly" in text_lower or "week" in text_lower:
        return "weekly"
    if "monthly" in text_lower or "month" in text_lower:
        return "monthly"

    return None


def detect_category(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["lunch", "dinner", "breakfast", "coffee", "food"]):
        return "Food"
    if any(word in text_lower for word in ["bus", "train", "taxi", "transport", "fuel"]):
        return "Transport"
    if any(word in text_lower for word in ["movie", "game", "entertainment"]):
        return "Entertainment"
    if any(word in text_lower for word in ["salary", "bonus", "income", "paycheck", "wage", "freelance","commission"]):
        return "Income"

    return "Other"


def extract_description(text: str) -> str:
    text_lower = text.lower()

    text_lower = re.sub(r'(\d[\d.,]*)', '', text_lower)

    # Remove common filler words
    text_lower = re.sub(r'\b(i|spent|buy|bought|paid|purchase|for|on|my|a|an|the)\b', '', text_lower)

    description = re.sub(r'\s+', ' ', text_lower).strip()
    return description if description else "No description"

def detect_transaction_type(text: str) -> tuple[str | None, str]:
    """
    Detects whether the message starts with:
    E, Expense, I, Income

    Returns:
        ("expense", cleaned_text)
        ("income", cleaned_text)
        (None, original_text)
    """

    text = text.strip()

    if text.lower().startswith("expense "):
        return "expense", text[8:].strip()

    if text.lower().startswith("income "):
        return "income", text[7:].strip()

    if text.lower().startswith("e "):
        return "expense", text[2:].strip()

    if text.lower().startswith("i "):
        return "income", text[2:].strip()

    return None, text

def infer_transaction_type(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in INCOME_KEYWORDS):
        return "income"

    return "expense"

def parse_message(text: str) -> Dict[str, Any]:
    transaction_type, text = detect_transaction_type(text)

    intent = detect_intent(text)
    amount = extract_amount(text)

    # Report requests don't require an amount
    if intent == "get_report":
        return {
            "intent": "get_report",
            "period": detect_report_period(text),
            "source": "text"
        }

    # Treat any message with an amount as an expense
    if intent == "unknown" and amount is not None:
        intent = "add_expense"

    # Expense messages require an amount
    if intent == "add_expense":
        if amount is None:
            return {
                "intent": "error",
                "message": "Amount not found",
                "source": "text"
            }

        return {
            "intent": "add_expense",
            "type": transaction_type or infer_transaction_type(text),
            "amount": amount,
            "category": detect_category(text),
            "description": extract_description(text),
            "source": "text"
        }

    return {
        "intent": "unknown",
        "source": "text"
    }