import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()

# =============================
# Paths (حسب هيكلتك)
# =============================
PROCESSED_CACHE = Path("data/processed/weather/openweather_cache.parquet")
FINAL_FORECAST_SELECTED = Path("data/final/weather_forecast_selected.parquet")

# =============================
# Cities mapping (لازم نفس city_id اللي اعتمدتيه)
# =============================
CITIES = [
    {"city_id": 1, "city_geo": "riyadh", "name": "Riyadh"},
    {"city_id": 2, "city_geo": "jeddah", "name": "Jeddah"},
    {"city_id": 3, "city_geo": "khobar", "name": "Al Khobar"},
    {"city_id": 4, "city_geo": "dammam", "name": "Dammam"},
]

# =============================
# 1) Fetch forecast + save raw cache to processed
# =============================
def fetch_openweather_forecast_save_cache():
    """
    تجيب Forecast كل 3 ساعات من OpenWeather وتخزنه كـ raw cache في processed
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")  # تأكدي الاسم نفس اللي في .env
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY not found. Add it to .env")

    rows = []
    for c in CITIES:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": c["name"],
            "appid": api_key,
            "units": "metric",
        }

        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        for item in data.get("list", []):
            weather0 = (item.get("weather") or [{}])[0]
            rows.append({
                "city_id": c["city_id"],
                "city_geo": c["city_geo"],
                "city_name": c["name"],
                "forecast_time": pd.to_datetime(item["dt"], unit="s", utc=True),
                "temp_c": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "weather_main": weather0.get("main"),
                "weather_desc": weather0.get("description"),
                "wind_speed": item.get("wind", {}).get("speed"),
                "source": "openweather",
                "updated_at": pd.Timestamp.utcnow(),
            })

    df_cache = pd.DataFrame(rows)

    PROCESSED_CACHE.parent.mkdir(parents=True, exist_ok=True)
    df_cache.to_parquet(PROCESSED_CACHE, index=False)

    print("✅ Saved processed cache:", PROCESSED_CACHE)
    return df_cache


# =============================
# 2) Load cache + save selected forecast to final
# =============================
def build_final_forecast_selected_from_cache():
    """
    يقرأ الكاش من processed ويطلع ملف final للأربع مدن فقط
    (مرتب + بدون تكرار + جاهز للاستخدام)
    """
    if not PROCESSED_CACHE.exists():
        raise FileNotFoundError(f"Cache not found: {PROCESSED_CACHE}. Run fetch_openweather_forecast_save_cache() first.")

    df = pd.read_parquet(PROCESSED_CACHE)

    # فلترة للأربع مدن (احتياط)
    allowed_ids = {c["city_id"] for c in CITIES}
    df = df[df["city_id"].isin(allowed_ids)].copy()

    # ترتيب + إزالة التكرارات (لو تكرر نفس الوقت لنفس المدينة)
    df = df.sort_values(["city_id", "forecast_time", "updated_at"])
    df = df.drop_duplicates(subset=["city_id", "forecast_time"], keep="last")

    FINAL_FORECAST_SELECTED.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(FINAL_FORECAST_SELECTED, index=False)

    print("✅ Saved final selected forecast:", FINAL_FORECAST_SELECTED)
    return df


# =============================
# Optional: one-shot run
# =============================
if __name__ == "__main__":
    fetch_openweather_forecast_save_cache()
    build_final_forecast_selected_from_cache()