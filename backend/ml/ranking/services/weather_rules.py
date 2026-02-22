def is_weather_ok(temp_c, user_min, user_max):
    if temp_c is None:
        return True
    return user_min <= temp_c <= user_max

def infer_environment_from_category(level1, level2, level3):
    text = " ".join([x for x in [level1, level2, level3] if x]).lower()

    outdoor_keywords = ["nature", "park", "landmark", "outdoor", "beach"]
    indoor_keywords = ["mall", "museum", "indoor", "shopping", "cinema"]

    if any(k in text for k in outdoor_keywords):
        return "outdoor"
    if any(k in text for k in indoor_keywords):
        return "indoor"
    return "mixed"
