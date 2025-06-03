from django.db import models

# Create your models here.

class Customer(models.Model):
    phone = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.customer.name} - {self.date} at {self.time}"