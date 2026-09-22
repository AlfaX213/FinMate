from app.services.sheets_service import get_gspread_client

client = get_gspread_client()

print("Connected!")

for sheet in client.openall():
    print(sheet.title)