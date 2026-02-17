import pandas as pd
from django.core.management.base import BaseCommand
from core_data.models import EventMode


class Command(BaseCommand):
    help = "Import Event Modes from data/final/event_modes.parquet"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="../data/final/event_modes.parquet",
            help="Path to event_modes.parquet",
        )

    def handle(self, *args, **options):
        path = options["path"]
        df = pd.read_parquet(path)

        created, updated = 0, 0

        for _, row in df.iterrows():

            mode_id = int(row["mode_id"])
            name = str(row["EventMode"]).strip()

            obj, was_created = EventMode.objects.update_or_create(
                mode_id=mode_id,
                defaults={"name": name}
            )

            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(
            f"✅ EventModes import done. created={created}, updated={updated}"
        ))