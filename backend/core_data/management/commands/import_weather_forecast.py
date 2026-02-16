import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import City, WeatherForecast


class Command(BaseCommand):
    help = "Import Weather Forecast from data/final/weather_forecast_selected.parquet"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/weather_forecast_selected.parquet",
            help="Path to weather_forecast_selected.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_parquet(path)

        created, updated, skipped = 0, 0, 0

        for _, row in df.iterrows():

            # ---------------------------
            # FK: City
            # ---------------------------
            city = None
            if not pd.isna(row.get("city_id")):
                try:
                    city = City.objects.filter(
                        city_id=int(row["city_id"])
                    ).first()
                except:
                    city = None

            if city is None:
                skipped += 1
                continue

            # ---------------------------
            # Forecast Time
            # ---------------------------
            forecast_time_value = None
            if not pd.isna(row.get("forecast_time")):
                try:
                    forecast_time_value = pd.to_datetime(
                        row.get("forecast_time")
                    )
                except:
                    skipped += 1
                    continue

            defaults = {
                "temp_c": (
                    None if pd.isna(row.get("temp_c"))
                    else float(row.get("temp_c"))
                ),
                "humidity": (
                    None if pd.isna(row.get("humidity"))
                    else float(row.get("humidity"))
                ),
                "wind_speed": (
                    None if pd.isna(row.get("wind_speed"))
                    else float(row.get("wind_speed"))
                ),
                "weather_main": (
                    None if pd.isna(row.get("weather_main"))
                    else str(row.get("weather_main")).strip()
                ),
                "weather_desc": (
                    None if pd.isna(row.get("weather_desc"))
                    else str(row.get("weather_desc")).strip()
                ),
                "source": (
                    None if pd.isna(row.get("source"))
                    else str(row.get("source")).strip()
                ),
            }

            obj, was_created = WeatherForecast.objects.update_or_create(
                city=city,
                forecast_time=forecast_time_value,
                defaults=defaults
            )

            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Weather Forecast import done. created={created}, updated={updated}, skipped={skipped}"
        ))