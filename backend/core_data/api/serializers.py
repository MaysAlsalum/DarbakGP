from rest_framework import serializers
from core_data.models import City, POICategory, POI, Event, WeatherForecast


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class POICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = POICategory
        fields = "__all__"


class POISerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    category = POICategorySerializer(read_only=True)

    class Meta:
        model = POI
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class WeatherForecastSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = WeatherForecast
        fields = "__all__"



class POIMapSerializer(serializers.ModelSerializer):
    # نخلي city و category كـ IDs بدل nested objects
    city_id = serializers.IntegerField(source="city.city_id", read_only=True)
    category_id = serializers.IntegerField(source="category.category_id", read_only=True)

    class Meta:
        model = POI
        fields = [
            "poi_id",
            "name",
            "latitude",
            "longitude",
            "rating",
            "city_id",
            "category_id",
        ]