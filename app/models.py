from django.contrib.auth.models import User
from django.db import models


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=255)

    def __str__(self):
        return 'Vehicle {}'.format(self.registration_number)


class Journey(models.Model):
    passengers = models.ManyToManyField(User)
    vehicle = models.ForeignKey(Vehicle, models.PROTECT)
    kilometers = models.FloatField()

    def __str__(self):
        return 'Journey {} on {}'.format(self.id, str(self.vehicle))