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
        data = yf.Ticker(stock.symbol)
        price = data.info.get('regularMarketPrice')
        if price:
            stock.price = price
            stock.save()
    except Exception as e:
        print(f"Error actualizando {stock.symbol}: {e}")

    return redirect('dashboard')
'''
@staff_member_required
def update_stock_price(request, pk):
    stock = get_object_or_404(Stock, pk=pk)

    try:
        ticker = yf.Ticker(stock.symbol)
        
        # Opción A: Más rápida y menos probable de ser bloqueada
        data = ticker.history(period="1d")
        
        if not data.empty:
            # Tomamos el último precio de cierre disponible
            price = data['Close'].iloc[-1]
            stock.price = price
            stock.save()
        else:
            # Si history falla, intentamos fast_info como respaldo
            price = ticker.fast_info.get('last_price')
            if price:
                stock.price = price
                stock.save()
                
    except Exception as e:
        # En Render, usa logging en lugar de print para ver los errores en la consola de logs
        import logging
        logging.error(f"Error actualizando {stock.symbol}: {e}")

    return redirect('dashboard')


















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