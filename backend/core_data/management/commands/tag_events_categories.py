from django.core.management.base import BaseCommand
from core_data.models import Event, POICategory

KEYWORDS = [
    (["معرض", "expo", "exhibition"], ("Arts & Culture",)),
    (["بطولة", "مباراة", "league", "cup"], ("Amusement & Leisure",)),
    (["مؤتمر", "conference", "summit"], ("Arts & Culture",)),
    (["حفلة", "concert", "festival"], ("Amusement & Leisure",)),
]

class Command(BaseCommand):
    help = "Auto-tag events with a POICategory based on keywords (MVP)."

    def handle(self, *args, **options):
        updated = 0

        for ev in Event.objects.all():
            text = (ev.name or "") + " " + (getattr(ev, "description", "") or "")
            text_lower = text.lower()

            chosen = None
            for keys, (level1,) in KEYWORDS:
                if any(k in text_lower for k in keys):
                    chosen = POICategory.objects.filter(level1=level1).first()
                    if chosen:
                        break

            if chosen and ev.category_id != chosen.category_id:
                ev.category = chosen
                ev.save(update_fields=["category"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Events tagged. updated={updated}"))
