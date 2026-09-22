import gspread # type: ignore
from datetime import datetime
from google.oauth2.service_account import Credentials  # type: ignore
from app.config import (
    GOOGLE_SHEET_NAME,
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_WORKSHEET_NAME,
)
import os

print("Loaded sheets_service from:", __file__)
print("Current working directory:", os.getcwd())


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_gspread_client():
    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=SCOPES
    )
    return gspread.authorize(credentials)


_worksheet_cache = None

def get_worksheet():
    global _worksheet_cache

    if _worksheet_cache:
        return _worksheet_cache

    client = get_gspread_client()

    print("Looking for spreadsheet:", GOOGLE_SHEET_NAME)
    print("Accessible spreadsheets:")

    for sheet in client.openall():
        print("-", sheet.title)

    spreadsheet = client.open(GOOGLE_SHEET_NAME)

    try:
        worksheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=GOOGLE_WORKSHEET_NAME,
            rows=1000,
            cols=10
        )
        worksheet.append_row([
            "Date",
            "Type",
            "Amount",
            "Category",
            "Description",
        ])

    _worksheet_cache = worksheet
    return worksheet


from datetime import datetime

def append_transaction_row(data: dict):
    worksheet = get_worksheet()

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("type", ""),
        data.get("amount", ""),
        data.get("category", ""),
        data.get("description", ""),
    ]

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )