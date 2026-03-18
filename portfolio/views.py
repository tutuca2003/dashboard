from django.shortcuts import render
from .models import Stock
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import redirect, get_object_or_404
import yfinance as yf  # pip install yfinance

'''
@staff_member_required
def update_stock_price(request, pk):
    stock = get_object_or_404(Stock, pk=pk)

    try:
        ticker = yf.Ticker(stock.symbol)
        # Pedimos solo el último día. Esto es MUCHO más rápido que .info
        df = ticker.history(period="1d")
        
        if not df.empty:
            # .iloc[-1] toma el último precio de cierre
            latest_price = df['Close'].iloc[-1]
            stock.price = latest_price
            stock.save()
        else:
            logger.warning(f"No se encontraron datos para {stock.symbol}")

    except Exception as e:
        logger.error(f"Error en Render al actualizar {stock.symbol}: {e}")

    return redirect('dashboard')

'''

from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Stock
import sheets_service 

@staff_member_required
def update_stock_price(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    try:
        sheet = sheets_service.conectar_sheet()
        celda = sheet.find(stock.symbol.upper())
        if celda:
            datos_fila = sheet.row_values(celda.row)
            # Ajuste de columnas: B=1, C=2, D=3
            stock.price = float(datos_fila[1].replace(',', '.')) if datos_fila[1] else stock.price  

@staff_member_required
def dashboard(request):
    stocks = Stock.objects.all().order_by('symbol')  # ← aquí se ordena

    # Obtener filtros desde GET
    strategy = request.GET.get('strategy')
    trade_status = request.GET.get('trade_status')
    analyzed = request.GET.get('analyzed')

    # Aplicar filtros
    if strategy:
        stocks = stocks.filter(strategy=strategy)
    if trade_status:
        stocks = stocks.filter(trade_status=trade_status)
    if analyzed in ['true', 'false']:
        stocks = stocks.filter(analyzed=(analyzed == 'true'))

    return render(request, "dashboard.html", {
        "stocks": stocks,
        "current_strategy": strategy,
        "current_trade_status": trade_status,
        "current_analyzed": analyzed,
    })