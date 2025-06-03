from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attractions/', views.attractions, name='attractions'),
    path('contact/', views.contact_view, name='contact'),
    path('bookings/', views.booking_view, name='bookings'),
]