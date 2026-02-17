import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import POICategory


class Command(BaseCommand):
    help = "Import POI Categories from data/final/poi_categories.parquet"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/poi_categories.parquet",
            help="Path to poi_categories.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_parquet(path)

        created, updated = 0, 0

        for _, row in df.iterrows():

            category_id = int(row["category_id"])

            level1 = (
                None if pd.isna(row.get("category_level1"))
                else str(row.get("category_level1")).strip()
            )

            level2 = (
                None if pd.isna(row.get("category_level2"))
                else str(row.get("category_level2")).strip()
            )

            level3 = (
                None if pd.isna(row.get("category_level3"))
                else str(row.get("category_level3")).strip()
            )

            obj, was_created = POICategory.objects.update_or_create(
                category_id=category_id,
                defaults={
                    "level1": level1,
                    "level2": level2,
                    "level3": level3,
                },
            )

            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Categories import done. created={created}, updated={updated}"
        ))