from django.db.models import Sum
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from app.models import Journey, Vehicle, User


class JourneyCreateView(CreateView):
    model = Journey
    fields = ['passengers', 'vehicle', 'kilometers']

    success_url = '/'


class VehicleStats(TemplateView):
    template_name = 'app/vehicle_stats.html'

    def get_context_data(self, **kwargs):
        vehicles = []

        for vehicle in Vehicle.objects.all().order_by('id'):
            total_km = vehicle.journey_set.aggregate(Sum('kilometers')).get('kilometers__sum')
            if total_km is None:
                total_km = 0

            vehicles.append({
                'registration_number': vehicle.registration_number,
                'total_km': total_km
            })

        return {'vehicles': vehicles}


class PassengerStats(TemplateView):
    template_name = 'app/passenger_stats.html'

    def get_context_data(self, **kwargs):
        journey_data = list(Journey.passengers.through.objects.values('user__username', 'journey__vehicle__registration_number').annotate(total_km=Sum('journey__kilometers')))

        return {
            'passenger_vehicles': journey_data
        }