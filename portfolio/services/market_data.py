'''
import yfinance as yf

def get_current_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1])
    except Exception as e:
        print("Error obteniendo precio:", e)
    return None
'''

import yfinance as yf

def get_stock_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Obtenemos el precio
        data = ticker.history(period="1d")
        price = float(data["Close"].iloc[-1]) if not data.empty else None
        # Obtenemos el nombre de la acción
        name = ticker.info.get("longName", symbol)  # Si no hay nombre, usamos el símbolo
        return price, name
    except Exception as e:
        print("Error obteniendo info:", e)
        return None, None