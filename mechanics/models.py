import re

from django.core.exceptions import ValidationError
from django.db import models


class Mechanic(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    rating = models.FloatField(default=0.0)
    is_open = models.BooleanField(default=True)
    services = models.JSONField(default=list, blank=True)

    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError({'name': 'Name is required.'})

        phone = self.phone.strip()
        if not re.fullmatch(r'^(\+\d{1,3})?\d{10,15}$', phone):
            raise ValidationError({'phone': 'Enter a valid phone number.'})

        if not self.location.strip():
            raise ValidationError({'location': 'Location is required.'})

        if not isinstance(self.services, list) or not self.services:
            raise ValidationError({'services': 'At least one service is required.'})

        if not 0 <= float(self.rating) <= 5:
            raise ValidationError({'rating': 'Rating must be between 0 and 5.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='service_requests')
    service = models.CharField(max_length=150)
    problem_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not self.customer_name.strip():
            raise ValidationError({'customer_name': 'Customer name is required.'})

        phone = self.customer_phone.strip()
        if not re.fullmatch(r'^(\+\d{1,3})?\d{10,15}$', phone):
            raise ValidationError({'customer_phone': 'Enter a valid customer phone number.'})

        if not re.fullmatch(r'^[A-Z]{2}[0-9]{2}[A-Z]{0,2}[0-9]{4}$', self.vehicle_number.upper()):
            raise ValidationError({'vehicle_number': 'Enter a valid vehicle number, e.g. MH12AB1234.'})

        service = self.service.strip().lower()
        if not service:
            raise ValidationError({'service': 'Service is required.'})
        if service not in [item.strip().lower() for item in self.mechanic.services if isinstance(item, str)]:
            raise ValidationError({'service': 'Invalid service for the selected mechanic.'})

        if not self.problem_description.strip():
            raise ValidationError({'problem_description': 'Problem description is required.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer_name} - {self.service}'
