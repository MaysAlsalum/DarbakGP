from planner.services.weather_service import get_today_weather
from planner.services.decision_engine import evaluate_weather_suitability


def adjust_pois_by_weather(user, city_id, pois):
    weather = get_today_weather(city_id)
    suitability = evaluate_weather_suitability(weather, user.profile)

    if not suitability["outdoor_ok"]:
        pois = pois.filter(is_indoor=True)

    return pois, suitability["reason"]
