import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import City

class Command(BaseCommand):
    help = "Import selected cities from data/final/selected_cities.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/selected_cities.csv",
            help="Path to selected_cities.csv",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_csv(path)

        # expected columns: city_id, city_geo, city_name_ar, region_name_ar
        created, updated = 0, 0

        for _, row in df.iterrows():
            obj, was_created = City.objects.update_or_create(
                city_id=int(row["city_id"]),
                defaults={
                    "city_geo": str(row["city_geo"]).strip(),
                    "city_name_ar": str(row["city_name_ar"]).strip(),
                    "region_name_ar": str(row["region_name_ar"]).strip(),
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Cities import done. created={created}, updated={updated}"
        ))