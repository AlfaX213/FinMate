from app.services.parser_service import parse_message

samples = [
    "I spent 25000 for lunch",
    "Bought coffee 18000",
    "Show my monthly report",
    "Weekly summary",
    "Hello there"
]

for text in samples:
    print(f"Input: {text}")
    print("Output:", parse_message(text))
    print("-" * 40)