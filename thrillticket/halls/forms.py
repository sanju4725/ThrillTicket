from django import forms
from .models import Booking, Customer
from django.forms.widgets import DateInput, TimeInput
from datetime import time, timedelta, datetime
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    mobile = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your Mobile (Optional)'})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time']

    def clean_time(self):
        booking_time = self.cleaned_data['time']
        if not time(11, 0) <= booking_time <= time(20, 0):
            raise ValidationError("Bookings must be between 11 AM and 8 PM.")
        return booking_time

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('date')
        booking_time = cleaned_data.get('time')

        if booking_date and booking_time:
            start_datetime = datetime.combine(booking_date, booking_time)
            end_datetime = start_datetime + timedelta(hours=2)

            overlapping_bookings = Booking.objects.filter(
                date=booking_date,
                time__gte=(start_datetime - timedelta(hours=2)).time(),
                time__lt=end_datetime.time()
            )

            if overlapping_bookings.exists():
                raise ValidationError("This time slot is already booked.")