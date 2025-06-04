from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attractions/', views.attractions, name='attractions'),
    path('contact/', views.contact_view, name='contact'),
    path('bookings/', views.booking_view, name='booking_view'),
    path('save_customer_details/', views.save_customer_details, name='save_customer_details'),
    path('calendar/<int:customer_id>/', views.calendar_view, name='calendar_view'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),
    path('book_slot/<int:customer_id>/', views.book_slot, name='book_slot'),
]