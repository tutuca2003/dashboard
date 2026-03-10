from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),
    #path('update-all-values/', views.update_all_values, name='update_all_values'),
    #path('dashboard/<str:strategy>/', views.dashboard, name='dashboard_strategy'),
    #path('dashboard/<str:strategy>/', views.dashboard, name='dashboard_strategy'),   
    path('update_price/<int:pk>/', views.update_stock_price, name='update_stock_price'),
]
