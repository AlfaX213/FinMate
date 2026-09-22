import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

# Load variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Define the structure Gemini must return
class Transaction(BaseModel):
    type: str
    amount: int
    category: str
    description: str


def parse_transaction(message: str) -> Transaction:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"""
        Analyze the following financial message:

        "{message}"

        Extract the transaction information.
        Determine whether it is an expense or income.
        Understand both English and Indonesian.

        Return:
        - type: "expense" or "income"
        - amount: numeric amount in Indonesian Rupiah
        - category: transaction category
        - description: short description of the transaction
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": Transaction,
        },
    )

    return response.parsed # type: ignore