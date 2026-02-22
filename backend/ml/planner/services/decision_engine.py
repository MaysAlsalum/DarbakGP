def evaluate_weather_suitability(weather, user_profile):
    """
    Decide if outdoor activities are suitable.
    """

    if not weather:
        return {"outdoor_ok": True, "reason": "No weather data available"}

    temp = weather.temp_c
    wind = weather.wind_speed
    humidity = weather.humidity

    # درجة الحرارة خارج نطاق تفضيل المستخدم
    if temp < user_profile.min_temp or temp > user_profile.max_temp:
        return {
            "outdoor_ok": False,
            "reason": "Temperature outside preferred range"
        }

    # رياح قوية
    if wind > 8:
        return {
            "outdoor_ok": False,
            "reason": "High wind speed"
        }

    # رطوبة عالية جدًا
    if humidity > 85:
        return {
            "outdoor_ok": False,
            "reason": "Very high humidity"
        }

    return {
        "outdoor_ok": True,
        "reason": "Weather suitable"
    }
