from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

# Create your views here.
def index(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                subject=f"New Contact from {name}",
                message=message,
                from_email=email,
                recipient_list=['info@thrillticket.com'],
            )
            return render(request, 'halls/index.html', {'form': ContactForm(), 'success': True})

    return render(request, 'halls/index.html', {'form': form})