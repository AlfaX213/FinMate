# Requirements
1. Python 3.x
2. Telegram account
3. Google account
4. Google Cloud project
5. Gemini API key
6. Google Sheets

# Steps on using the Bot

## Windows
**1. In Powershell:** 
`python -m venv wenv
.\wenv\Scripts\Activate.ps1`

**2. Install dependencies**
`pip install -r requirements.txt`

**3. Configure Telegram Bot**
- Search BotFather in Telegram and chat with it.
- Type /newbot and it'll set up a bot for you.
- Copy the generated token and put it in .env

**4. Configure Sheets**
- Create a Google Cloud project.
- Enable Google Sheets API.
- Enable Google Drive API.
- Create a service account.
- Create a JSON key.
- Place the JSON inside:
`credentials/google-service-account.json`

**5. Configure Gemini**
- Open Google AI Studio.
- Sign in with your Google account.
- Open the API Keys page.
- Create a new Gemini API key.
- Copy the generated API key.
- Input the API key to the .env.
