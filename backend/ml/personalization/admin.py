from django.contrib import admin
from .models import UserProfile, UserCategoryPreference


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "budget_level",
        "min_temp",
        "max_temp",
        "outdoor_preference",
        "walk_tolerance",
        "group_type",
    )


@admin.register(UserCategoryPreference)
class UserCategoryPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "category",
        "weight",
        "created_at",
    )
