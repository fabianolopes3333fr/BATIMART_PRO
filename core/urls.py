from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:page_slug>/', views.page, name='page'),
    path('<slug:client_slug>/', views.home, name='client_home'),
    path('<slug:client_slug>/<slug:page_slug>/', views.page, name='client_page'),
]