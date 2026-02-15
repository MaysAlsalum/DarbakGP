from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# نستورد وظائف OpenWeather 
from backend.src.weather.openweather_service import (
    fetch_openweather_forecast_save_cache,
    build_final_forecast_selected_from_cache,
)

app = FastAPI(title="Darbak API")

scheduler = BackgroundScheduler()


def weather_job():
    # 1) يجلب forecast ويحفظه في processed/openweather_cache.parquet
    fetch_openweather_forecast_save_cache()
    # 2) يبني نسخة final للأربع مدن ويحفظها في final/weather_forecast_selected.parquet
    build_final_forecast_selected_from_cache()
    print("✅ Weather job done (OpenWeather updated).")


@app.on_event("startup")
def start_scheduler():
    # تشغيل أول تحديث فور تشغيل السيرفر
    weather_job()

    # بعدها كل 3 ساعات
    scheduler.add_job(
        weather_job,
        trigger=IntervalTrigger(hours=3),
        id="openweather_3h_job",
        replace_existing=True,
    )
    scheduler.start()
    print("✅ Scheduler started (every 3 hours).")


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
    print("🛑 Scheduler stopped.")
    


FORECAST_FILE = Path("data/final/weather_forecast_selected.parquet")

@app.get("/weather/forecast")
def get_weather_forecast():
    if not FORECAST_FILE.exists():
        return {"error": "forecast file not found", "path": str(FORECAST_FILE)}

    df = pd.read_parquet(FORECAST_FILE)

    # ترتيب للعرض (اختياري لكن مفيد)
    if "forecast_time" in df.columns:
        df = df.sort_values(["city_id", "forecast_time"])

    updated_at = None
    if "updated_at" in df.columns and not df.empty:
        updated_at = str(df["updated_at"].max())

    return {
        "updated_at": updated_at,
        "count": int(len(df)),
        "rows": df.to_dict(orient="records"),
    }

