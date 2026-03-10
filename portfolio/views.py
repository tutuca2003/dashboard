from django.shortcuts import render
from .models import Stock
from django.contrib.admin.views.decorators import staff_member_required

'''
@staff_member_required
def dashboard(request):
    stocks = Stock.objects.all()

    return render(request, "dashboard.html", {
        "stocks": stocks
    })
'''

from django.shortcuts import redirect, get_object_or_404
import yfinance as yf  # pip install yfinance


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




from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Stock

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