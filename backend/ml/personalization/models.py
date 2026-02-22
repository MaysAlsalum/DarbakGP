from django.db import models

# Create your models here.


from django.contrib.auth.models import User
from core_data.models import POICategory



class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # Budget: 1 (low) → 5 (high)
    budget_level = models.IntegerField(default=3)

    # Comfortable temperature range
    min_temp = models.FloatField(default=18)
    max_temp = models.FloatField(default=32)

    # Outdoor preference (0 → 1)
    outdoor_preference = models.FloatField(default=0.5)

    WALK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    walk_tolerance = models.CharField(
        max_length=10,
        choices=WALK_CHOICES,
        default="medium"
    )

    GROUP_CHOICES = [
        ("solo", "Solo"),
        ("family", "Family"),
        ("friends", "Friends"),
    ]
    group_type = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        default="solo"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return f"Profile for {self.user.username}"


class UserCategoryPreference(models.Model):
    """
    User selects a specific POI category (can be level2/level3).
    Stored as FK to POICategory (no manual mapping).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category_preferences")
    category = models.ForeignKey(POICategory, on_delete=models.CASCADE, related_name="preferred_by")
    weight = models.FloatField(default=1.0)  # 0.5..3 (حسب قوة الاهتمام)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_category_preferences"
        unique_together = ("user", "category")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.category_id} (w={self.weight})"
