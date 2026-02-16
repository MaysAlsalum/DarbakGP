import pandas as pd
import re
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

        for _, row in df.iterrows():
            poi_id = str(row.get("poi_id") or "").strip()
            name = str(row.get("name") or "").strip()

            if not poi_id or not name:
                skipped += 1
                continue

            # ---------------------------
            # FK: City
            # ---------------------------
            city = None
            if "city_id" in df.columns and not pd.isna(row.get("city_id")):
                try:
                    city = City.objects.filter(
                        city_id=int(row["city_id"])
                    ).first()
                except:
                    city = None

            # ---------------------------
            # FK: Category
            # ---------------------------
            category = None
            if "category_id" in df.columns and not pd.isna(row.get("category_id")):
                try:
                    category = POICategory.objects.filter(
                        category_id=int(row["category_id"])
                    ).first()
                except:
                    category = None

            # ---------------------------
            # تنظيف rating
            # ---------------------------
            rating_value = None
            raw_rating = row.get("rating")
            if not pd.isna(raw_rating):
                try:
                    rating_value = float(raw_rating)
                except:
                    rating_value = None

            # ---------------------------
            # تنظيف rating_count
            # ---------------------------
            rating_count_value = None
            raw_rating_count = row.get("rating_count")
            if not pd.isna(raw_rating_count):
                try:
                    rating_count_value = int(float(raw_rating_count))
                except:
                    rating_count_value = None

            # ---------------------------
            # تنظيف traffic_score
            # ---------------------------
            traffic_score_value = None
            raw_traffic = row.get("traffic_score")
            if not pd.isna(raw_traffic):
                try:
                    traffic_score_value = float(raw_traffic)
                except:
                    traffic_score_value = None

            # ---------------------------
            # تنظيف time_spent (الأهم 🔥)
            # ---------------------------
            raw_time_spent = row.get("time_spent")
            time_spent_value = None

            if not pd.isna(raw_time_spent):
                try:
                    time_spent_value = float(raw_time_spent)
                except:
                    # استخراج أول رقم من النص
                    match = re.search(r"\d+(\.\d+)?", str(raw_time_spent))
                    if match:
                        time_spent_value = float(match.group())

            # ---------------------------
            # latitude / longitude
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

            # ---------------------------
            # defaults dict
            # ---------------------------
            defaults = {
                "name": name,
                "address": (
                    None if pd.isna(row.get("address"))
                    else str(row.get("address")).strip()
                ),
                "latitude": latitude_value or 0.0,
                "longitude": longitude_value or 0.0,
                "phone": (
                    None if pd.isna(row.get("phone"))
                    else str(row.get("phone")).strip()
                ),
                "website_domain": (
                    None if pd.isna(row.get("website_domain"))
                    else str(row.get("website_domain")).strip()
                ),
                "rating": rating_value,
                "rating_count": rating_count_value,
                "traffic_score": traffic_score_value,
                "time_spent": time_spent_value,
                "source": (
                    None if pd.isna(row.get("source"))
                    else str(row.get("source")).strip()
                ),
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