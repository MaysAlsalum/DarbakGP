import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import City, Event


class Command(BaseCommand):
    help = "Import Events from data/final/events_selected.parquet"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/events_selected.parquet",
            help="Path to events_selected.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_parquet(path)

        created, updated, skipped = 0, 0, 0

        for _, row in df.iterrows():
            name = str(row.get("name") or "").strip()

            if not name:
                skipped += 1
                continue

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

            # ---------------------------
            # Dates
            # ---------------------------
            start_date_value = None
            if not pd.isna(row.get("start_date")):
                try:
                    start_date_value = pd.to_datetime(row.get("start_date")).date()
                except:
                    start_date_value = None

            end_date_value = None
            if not pd.isna(row.get("end_date")):
                try:
                    end_date_value = pd.to_datetime(row.get("end_date")).date()
                except:
                    end_date_value = None

            # ---------------------------
            # Latitude / Longitude
            # ---------------------------
            latitude_value = None
            if not pd.isna(row.get("latitude")):
                try:
                    latitude_value = float(row.get("latitude"))
                except:
                    latitude_value = None

            longitude_value = None
            if not pd.isna(row.get("longitude")):
                try:
                    longitude_value = float(row.get("longitude"))
                except:
                    longitude_value = None

            defaults = {
                "city": city,
                "start_date": start_date_value,
                "end_date": end_date_value,
                "source": (
                    None if pd.isna(row.get("source"))
                    else str(row.get("source")).strip()
                ),
            }

            obj, was_created = Event.objects.update_or_create(
                name=name,
                defaults=defaults
            )

            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Events import done. created={created}, updated={updated}, skipped={skipped}"
        ))