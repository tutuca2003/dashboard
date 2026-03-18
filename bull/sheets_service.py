'''import os
import json
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings


def conectar_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # 1. Intenta leer la variable de Render (si existe)
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDS')
    
    if creds_json:
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=scope)
    else:
        # 2. Si no hay variable (estás en tu PC), usa el archivo físico
        # 'google_key.json' debe estar en la carpeta principal de STOCKS
        ruta_archivo = os.path.join(settings.BASE_DIR, 'google_key.json')
        creds = Credentials.from_service_account_file(ruta_archivo, scopes=scope)
    
    client = gspread.authorize(creds)
    # Abre la hoja "Stock" (según tu captura de pantalla)
    return client.open("Stock").sheet1

'''
import gspread
import os
import json
from google.oauth2.service_account import Credentials

def conectar_sheet():
    # Definimos los permisos necesarios
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # 1. Intentamos leer desde la Variable de Entorno (Render)
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDS')
    
    if creds_json:
        # Render: Convertimos el texto de la variable en un diccionario
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=scope)
    else:
        # Local: Usamos el archivo físico si no existe la variable
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_json = os.path.join(base_dir, 'google_key.json')
        creds = Credentials.from_service_account_file(ruta_json, scopes=scope)
    
    client = gspread.authorize(creds)
    
    # Usa el nombre exacto de tu Sheet aquí
    return client.open("Stock").get_worksheet(0)