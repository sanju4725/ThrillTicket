from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    mobile = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your Mobile (Optional)'})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))