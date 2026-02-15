import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import City, POICategory, POI

class Command(BaseCommand):
    help = "Import POIs from data/final/poi_selected.parquet"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/poi_selected.parquet",
            help="Path to poi_selected.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_parquet(path)

        created, updated, skipped = 0, 0, 0

        # IMPORTANT: adjust these column names if yours differ
        # expected: poi_id, name, address, latitude, longitude, city_id, category_id, rating, rating_count, traffic_score, time_spent, phone, website_domain, source

        for _, row in df.iterrows():
            poi_id = str(row.get("poi_id") or "").strip()
            name = str(row.get("name") or "").strip()

            if not poi_id or not name:
                skipped += 1
                continue


            # Mapping based on locality
            locality_value = str(row.get("locality") or "").strip().lower()

            city = None
            if locality_value:
                city = City.objects.filter(city_geo=locality_value).first()

            category = None
            if "category_id" in df.columns and not pd.isna(row.get("category_id")):
                category = POICategory.objects.filter(category_id=int(row["category_id"])).first()

            defaults = {
                "name": name,
                "address": (None if pd.isna(row.get("address")) else str(row.get("address")).strip()),
                "latitude": float(row["latitude"]) if not pd.isna(row.get("latitude")) else 0.0,
                "longitude": float(row["longitude"]) if not pd.isna(row.get("longitude")) else 0.0,
                "phone": (None if pd.isna(row.get("phone")) else str(row.get("phone")).strip()),
                "website_domain": (None if pd.isna(row.get("website_domain")) else str(row.get("website_domain")).strip()),
                "rating": (None if pd.isna(row.get("rating")) else float(row.get("rating"))),
                "rating_count": (None if pd.isna(row.get("rating_count")) else int(row.get("rating_count"))),
                "traffic_score": (None if pd.isna(row.get("traffic_score")) else float(row.get("traffic_score"))),
                "time_spent": (None if pd.isna(row.get("time_spent")) else float(row.get("time_spent"))),
                "source": (None if pd.isna(row.get("source")) else str(row.get("source")).strip()),
                "city": city,
                "category": category,
            }

            obj, was_created = POI.objects.update_or_create(
                poi_id=poi_id,
                defaults=defaults
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ POIs import done. created={created}, updated={updated}, skipped={skipped}"
        ))