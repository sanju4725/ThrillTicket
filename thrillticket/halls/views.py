from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from .forms import BookingForm, ContactForm
from .models import Booking, Customer
from django.db.models import Count
from datetime import date, datetime, timedelta, time as dt_time
from django.http import JsonResponse



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
        phone = request.POST.get('phone')
        customer = Customer.objects.filter(phone=phone).first()
        if customer:
            # Proceed to calendar view
            return redirect('calendar_view', customer_id=customer.phone)
        else:
            # Prompt for name and email
            return render(request, 'halls/enter_details.html', {'phone': phone})
    return render(request, 'halls/booking_start.html')

def save_customer_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Try to find customer by email first
        customer = Customer.objects.filter(email=email).first()
        if customer:
            # Update phone if not set
            if customer.phone != phone:
                customer.phone = phone
                customer.save()
        else:
            customer = Customer.objects.create(name=name, email=email, phone=phone)

        return redirect('calendar_view', customer_id=customer.phone)
    return redirect('booking_view')

def calendar_view(request, customer_id):
    bookings = Booking.objects.values('date').annotate(count=Count('id'))
    booking_data = {b['date']: b['count'] for b in bookings}
    return render(request, 'halls/calendar.html', {'booking_data': booking_data, 'customer_id': customer_id})

def get_available_slots(request):
    date_str = request.GET.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    existing_bookings = Booking.objects.filter(date=date_obj).values_list('time', flat=True)
    all_slots = [dtime(hour=h) for h in range(11, 20, 2)]  # 11 AM to 7 PM
    available_slots = []
    for slot in all_slots:
        slot_end = (datetime.combine(date_obj, slot) + timedelta(hours=2)).time()
        overlap = Booking.objects.filter(date=date_obj, time__lt=slot_end, time__gte=slot).exists()
        if not overlap:
            available_slots.append(slot.strftime('%H:%M'))
    return JsonResponse({'slots': available_slots})

def book_slot(request, customer_id):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        customer = Customer.objects.get(id=customer_id)
        Booking.objects.create(customer=customer, date=date_obj, time=time_obj)
        # Send confirmation email
        subject = 'ThrillTicket Booking Confirmation'
        message = f"Hi {customer.name},\n\nYour visit is booked for {date_obj} at {time_obj}.\n\nSee you soon!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer.email])
        return render(request, 'halls/booking_success.html', {'name': customer.name})
    return redirect('calendar_view', customer_id=customer_id)