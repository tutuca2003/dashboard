import os
import json
import gspread
from google.oauth2.service_account import Credentials

def conectar_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Intenta leer de Render, si no, del archivo local
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDS')
    
    if creds_json:
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=scope)
    else:
        creds = Credentials.from_service_account_file('google_key.json', scopes=scope)
    
    client = gspread.authorize(creds)
    # CAMBIA ESTO por el nombre de tu Excel
    return client.open("Stock").sheet1