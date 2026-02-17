import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import City, District


class Command(BaseCommand):
    help = "Import Districts and link them to City by city_id"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/districts_selected.parquet",
            help="Path to districts_selected.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]

        df = pd.read_parquet(path)

        created, updated, skipped = 0, 0, 0

        for _, row in df.iterrows():

            # 1️⃣ نتأكد عندنا اسم حي
            if pd.isna(row.get("district_name_ar")):
                skipped += 1
                continue

            district_name_ar = str(row["district_name_ar"]).strip()

            # 2️⃣ نجيب المدينة عن طريق city_id
            city = None
            if not pd.isna(row.get("city_id")):
                try:
                    city = City.objects.get(city_id=int(row["city_id"]))
                except City.DoesNotExist:
                    skipped += 1
                    continue

            if city is None:
                skipped += 1
                continue

            # 3️⃣ نحضر القيم الإضافية
            district_name_en = (
                None
                if pd.isna(row.get("district_name_en"))
                else str(row["district_name_en"]).strip()
            )

            latitude = (
                None
                if pd.isna(row.get("latitude"))
                else float(row["latitude"])
            )

            longitude = (
                None
                if pd.isna(row.get("longitude"))
                else float(row["longitude"])
            )

            # 4️⃣ نعمل update_or_create عشان ما يصير تكرار
            obj, was_created = District.objects.update_or_create(
                district_name_ar=district_name_ar,
                city=city,  # 🔥 الربط الحقيقي هنا
                defaults={
                    "district_name_en": district_name_en,
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Districts import done. created={created}, updated={updated}, skipped={skipped}"
        ))