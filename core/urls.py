from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('<slug:client_slug>/', views.render_page, name='render_page'),
    path('<slug:client_slug>/<slug:page_slug>/', views.render_page, name='page')
]