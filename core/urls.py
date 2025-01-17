from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Adicione outras URLs específicas do core aqui
]