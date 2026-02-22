from rest_framework import serializers
from core_data.models import POICategory
from ml.personalization.models import UserCategoryPreference

class CategoryNodeSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = POICategory
        fields = ["category_id", "level1", "level2", "level3", "source", "label"]

    def get_label(self, obj):
        # عرض نهائي للمستخدم: level1 > level2 > level3 (بدون None)
        parts = [obj.level1, obj.level2, obj.level3]
        return " > ".join([p for p in parts if p])


class UserCategoryPreferenceSerializer(serializers.ModelSerializer):
    category_label = serializers.SerializerMethodField()

    class Meta:
        model = UserCategoryPreference
        fields = ["id", "category", "category_label", "weight", "created_at"]

    def get_category_label(self, obj):
        parts = [obj.category.level1, obj.category.level2, obj.category.level3]
        return " > ".join([p for p in parts if p])
    




from rest_framework import serializers


class UserPreferenceItemSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    weight = serializers.FloatField(default=1.0)


class UserPreferencesRequestSerializer(serializers.Serializer):
    items = UserPreferenceItemSerializer(many=True)