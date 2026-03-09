'''
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Stock
from django.db.models import Case, When, Value, IntegerField

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    return render(request, 'stock_detail.html', {'stock': stock})

from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Stock
from .services.market_data import get_stock_info

def update_all_values(request):
    stocks = Stock.objects.all()
    updated = 0

    for stock in stocks:
        # Obtener precio y nombre
        price, name = get_stock_info(stock.symbol)
        if price:
            stock.price = price
        if name:
            stock.name = name  # Guardamos el nombre en la DB

        # Calcular Fair Values
        stock.fv_simple = stock.price * 1.1
        stock.fv_dcf = stock.price * 1.2
        stock.fv_avg = (stock.fv_simple + stock.fv_dcf) / 2

        stock.save()
        updated += 1

    messages.success(request, f"Valores actualizados para {updated} acciones.")
    return redirect('dashboard')


def dashboard(request, strategy=None):

    stocks = Stock.objects.all()

    # filtro estrategia
    if strategy:
        stocks = stocks.filter(strategy=strategy)

    # filtro trade
    trade_filter = request.GET.get("trade")
    if trade_filter:
        trades = trade_filter.split(",")
        stocks = stocks.filter(trade_status__in=trades)

    # Orden personalizado: buy -> sell -> none, y dentro de cada grupo analizada primero
    order_case = Case(
        When(trade_status='buy', then=Value(0)),
        When(trade_status='sell', then=Value(1)),
        When(trade_status='none', then=Value(2)),
        output_field=IntegerField()
    )

    stocks = stocks.order_by(order_case, '-analyzed', 'symbol')

    return render(request, "dashboard.html", {
        "stocks": stocks,
        "current_strategy": strategy,
        "trade_filter": trade_filter
    })

'''

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from .models import Stock
from .services.market_data import get_stock_info


'''def dashboard(request, strategy=None):
    # Obtener todas las acciones
    stocks = Stock.objects.all()

    # Filtrar por estrategia si se indica
    if strategy:
        stocks = stocks.filter(strategy=strategy)

    # Orden personalizado: buy → sell → none, dentro de cada grupo primero analizadas
    order_case = Case(
        When(trade_status='buy', then=Value(0)),
        When(trade_status='sell', then=Value(1)),
        When(trade_status='none', then=Value(2)),
        output_field=IntegerField()
    )

    # Aplicar orden
    stocks = stocks.order_by(order_case, '-analyzed', 'symbol')

    return render(request, "dashboard.html", {
        "stocks": stocks,
        "current_strategy": strategy
    })
'''

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    return render(request, 'stock_detail.html', {'stock': stock})


def update_all_values(request):
    stocks = Stock.objects.all()
    updated = 0

    for stock in stocks:
        # Obtener precio y nombre
        price, name = get_stock_info(stock.symbol)

        print("SYMBOL:", stock.symbol, "PRICE:", price)

        if price:
            stock.price = price
        if name:
            stock.name = name

        # Calcular Fair Values
        stock.fv_simple = stock.price * 1.1
        stock.fv_dcf = stock.price * 1.2
        stock.fv_avg = (stock.fv_simple + stock.fv_dcf) / 2

        stock.save()
        updated += 1

    messages.success(request, f"Valores actualizados para {updated} acciones.")
    return redirect('dashboard')

from django.db.models import Case, When, Value, IntegerField

def dashboard(request, strategy=None):
    stocks = Stock.objects.all()

    if strategy:
        stocks = stocks.filter(strategy=strategy)

    # Prioridad: analizadas primero
    analyzed_case = Case(
        When(analyzed=True, then=Value(0)),
        When(analyzed=False, then=Value(1)),
        output_field=IntegerField()
    )

    # Prioridad trade_status
    trade_case = Case(
        When(trade_status='buy', then=Value(0)),
        When(trade_status='sell', then=Value(1)),
        When(trade_status='none', then=Value(2)),
        output_field=IntegerField()
    )

    # Orden final: primero analizadas, luego trade_status, luego símbolo
    stocks = stocks.order_by(analyzed_case, trade_case, 'symbol')

    return render(request, "dashboard.html", {
        "stocks": stocks,
        "current_strategy": strategy
    })