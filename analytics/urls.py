from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('map/', views.map, name='map'),
    path('predictions/', views.predictions, name='predictions'),
    path('products/', views.products, name='products'),
    path('stores/', views.stores, name='stores'),
]