from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

def index(request):
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