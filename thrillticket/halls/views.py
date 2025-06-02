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