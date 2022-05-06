from django.test import TestCase
from django.urls import reverse

from app.models import User, Journey, Vehicle


class TestStats(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        vehicle1 = Vehicle.objects.create(registration_number='vehicle1')
        vehicle2 = Vehicle.objects.create(registration_number='vehicle2')

        journey1 = Journey.objects.create(
            vehicle=vehicle1,
            kilometers=50
        )
        journey1.passengers.set([user1, user2])
        journey2 = Journey.objects.create(
            vehicle=vehicle2,
            kilometers=22
        )
        journey2.passengers.set([user1])

    def test_vehicle_stats(self):
        response = self.client.get(reverse('vehicle_stats'))

        expected_vehicle_stats = [
            {'registration_number': 'vehicle1', 'total_km': 50},
            {'registration_number': 'vehicle2', 'total_km': 22}
        ]

        self.assertEquals(response.context['vehicles'], expected_vehicle_stats)

    def test_passenger_stats(self):
        response = self.client.get(reverse('passenger_stats'))

        expected_passenger_stats = [
            {
                'user__username': 'user1',
                'journey__vehicle__registration_number': 'vehicle1',
                'total_km': 50
            },
            {
                'user__username': 'user1',
                'journey__vehicle__registration_number': 'vehicle2',
                'total_km': 22
            },
            {
                'user__username': 'user2',
                'journey__vehicle__registration_number': 'vehicle1',
                'total_km': 50
            },
        ]

        self.assertEquals(response.context['passenger_vehicles'], expected_passenger_stats)
