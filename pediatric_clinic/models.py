from django.db import models

# Create your models here.
from django.db import models


class Patient(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10)
    birthdate = models.DateField(null=True)
    polio_vaccine = models.CharField(max_length=255)
    polio_vaccine_date = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
            if Booking.objects.filter(patient=self).exists() and self.polio_vaccine != 'vaccinated':
                self.polio_vaccine = 'pending'
            super().save(*args, **kwargs)

class Available_date(models.Model):
    date = models.DateField()

  


class Booking(models.Model):
    date = models.ForeignKey(Available_date, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.name
