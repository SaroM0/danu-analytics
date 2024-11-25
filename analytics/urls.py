from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('map/', views.map, name='map'),
    path('predictions/', views.predictions, name='predictions'),
    path('products/', views.products, name='products'),
    path('stores/', views.stores, name='stores'),
    path('get-city-data/<str:city_name>/', views.get_city_data, name='get_city_data'),
    path('get-global-data/', views.get_global_data_api, name='get_global_data'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('filter-product-weekday-sales', views.filter_product_weekday_sales, name='filter_product_weekday_sales'),
]   
