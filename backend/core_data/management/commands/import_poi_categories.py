import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import POICategory

class Command(BaseCommand):
    help = "Import POI categories from data/final/poi_categories.parquet"

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

        # expected columns: category_id, level1, level2, level3, source
        created, updated = 0, 0

        for _, row in df.iterrows():
            cid = int(row["category_id"])
            obj, was_created = POICategory.objects.update_or_create(
                category_id=cid,
                defaults={
                    "level1": str(row.get("level1") or "").strip(),
                    "level2": (None if pd.isna(row.get("level2")) else str(row.get("level2")).strip()),
                    "level3": (None if pd.isna(row.get("level3")) else str(row.get("level3")).strip()),
                    "source": str(row.get("source") or "").strip(),
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ POI categories import done. created={created}, updated={updated}"
        ))