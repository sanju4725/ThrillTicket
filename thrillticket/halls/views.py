from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from .forms import BookingForm, ContactForm
from .models import Booking, Customer
from django.db.models import Count
from datetime import date, datetime, timedelta, time as dt_time



def index(request):
    # ✅ Review Email Trigger (simplified): send review emails for past bookings
    today = now().date()
    past_bookings = Booking.objects.filter(date__lt=today)

    for booking in past_bookings:
        customer = booking.customer
        # Optional: Add logic to prevent re-sending (e.g., booking.review_sent flag)
        subject = "How was your ThrillTicket experience?"
        message = f"""
Hi {customer.name},

You faced the horrors… now tell us what you think!  
Leave a review at https://thrillticket.com/reviews

We’d love to hear your scream-level feedback 💀

– ThrillTicket Team
"""
        send_mail(subject, message, 'info@thrillticket.com', [customer.email])

    # Handle contact form (same view as home)
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data.get('mobile', 'Not provided')
            message = form.cleaned_data['message']

            full_message = f"""
New contact form submission from ThrillTicket:

Name: {name}
Email: {email}
Mobile: {mobile or 'Not provided'}

Message:
{message}
            """.strip()

            send_mail(
                subject=f"[ThrillTicket] Message from {name}",
                message=full_message,
                from_email=email,
                recipient_list=['info@thrillticket.com'],
            )
            return render(request, 'halls/index.html', {'form': ContactForm(), 'success': True})

    return render(request, 'halls/index.html', {'form': form})

def attractions(request):
    attractions_data = [
        {
            "name": "Maze of Shadows",
            "icon": "👹",
            "image": "images/maze-of-shadows.jpg",
            "description": "A pitch-black labyrinth where shadows move, and so do your fears.",
            "testimonials": [
                {"text": "I almost ran straight into a wall. Terrifying!", "author": "Sara M."},
                {"text": "Pure darkness. I never screamed so much in my life.", "author": "Kevin T."}
            ]
        },
        {
            "name": "Zombie Alley",
            "icon": "🧟",
            "image": "images/zombie-alley.jpg",
            "description": "A foggy street crawling with the undead — and only one way out.",
            "testimonials": [
                {"text": "The jump scares were nonstop. Loved every second.", "author": "Priya N."}
            ]
        },
        {
            "name": "Hall of Screams",
            "icon": "🎭",
            "image": "images/hall-of-screams.jpg",
            "description": "A distorted funhouse where echoes of terror follow you through each twist.",
            "testimonials": [
                {"text": "Clowns. Mirrors. Screams. 10/10 horror.", "author": "Eli V."}
            ]
        },
        {
            "name": "The Butcher’s Basement",
            "icon": "🩸",
            "image": "images/butcher-basement.jpg",
            "description": "The blood-stained dungeon of the deranged butcher — and his cleaver.",
            "testimonials": [
                {"text": "Chainsaws? Really? I nearly fainted.", "author": "Joan K."}
            ]
        }
    ]
    return render(request, 'halls/attractions.html', {'attractions': attractions_data})

def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data.get('mobile', 'Not provided')
            message = form.cleaned_data['message']

            full_message = f"""
New contact form submission from ThrillTicket:

Name: {name}
Email: {email}
Mobile: {mobile or 'Not provided'}

Message:
{message}
            """.strip()

            send_mail(
                subject=f"[ThrillTicket] Message from {name}",
                message=full_message,
                from_email=email,
                recipient_list=['info@thrillticket.com'],
            )
            return render(request, 'halls/contact.html', {'form': ContactForm(), 'success': True})

    return render(request, 'halls/contact.html', {'form': form})

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            booking_date = form.cleaned_data['date']
            booking_time = form.cleaned_data['time']

            # Enforce booking time constraints
            if not dt_time(11, 0) <= booking_time <= dt_time(20, 0):
                form.add_error('time', 'Bookings are allowed only between 11 AM and 8 PM.')
            else:
                # Check for overlapping bookings (2-hour slots)
                overlap_start = (datetime.combine(booking_date, booking_time) - timedelta(hours=2)).time()
                overlap_end = (datetime.combine(booking_date, booking_time) + timedelta(hours=2)).time()
                overlapping = Booking.objects.filter(
                    date=booking_date,
                    time__gte=overlap_start,
                    time__lt=overlap_end
                )
                if overlapping.exists():
                    form.add_error('time', 'This time slot overlaps with an existing booking.')
                else:
                    # Get or create customer
                    customer, created = Customer.objects.get_or_create(
                        email=email,
                        defaults={'name': name, 'phone': phone}
                    )
                    Booking.objects.create(
                        customer=customer,
                        date=booking_date,
                        time=booking_time
                    )

                    # Send booking confirmation
                    subject = 'ThrillTicket Booking Confirmation'
                    message = f"Hi {name},\n\nYour visit is booked for {booking_date} at {booking_time}.\n\nSee you soon!"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

                    return render(request, 'halls/booking_success.html', {'name': name})
    else:
        form = BookingForm()

    # Prepare booking data for the calendar
    bookings = Booking.objects.values('date').annotate(count=Count('id'))
    booking_data = {b['date'].strftime('%Y-%m-%d'): b['count'] for b in bookings}

    return render(request, 'halls/bookings.html', {'form': form, 'booking_data': booking_data})