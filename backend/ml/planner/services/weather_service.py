from core_data.models import WeatherForecast
from django.utils import timezone

def get_today_weather(city_id):
    """
    Returns latest forecast record for today.
    """
    today = timezone.now().date()

    forecast = (
        WeatherForecast.objects
        .filter(city__city_id=city_id, forecast_time__date=today)
        .order_by("forecast_time")
        .first()
    )

    return forecast

