from django.contrib import admin

# Register your models here.


from .models import City, District, POICategory, POI, Event, WeatherContext, WeatherForecast


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_id", "city_geo", "city_name_ar", "region_name_ar")
    search_fields = ("city_geo", "city_name_ar", "region_name_ar")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("district_id", "district_name", "city")
    search_fields = ("district_name",)
    list_filter = ("city",)


@admin.register(POICategory)
class POICategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "level1", "level2", "level3", "source")
    search_fields = ("level1", "level2", "level3", "source")
    list_filter = ("source", "level1")


@admin.register(POI)
class POIAdmin(admin.ModelAdmin):
    list_display = ("poi_id", "name", "city", "category", "rating", "rating_count", "source")
    search_fields = ("poi_id", "name", "address")
    list_filter = ("city", "source", "category")
    ordering = ("-rating",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_id", "name", "city", "start_date", "end_date", "event_mode", "source")
    search_fields = ("name",)
    list_filter = ("city", "event_mode", "source")


@admin.register(WeatherContext)
class WeatherContextAdmin(admin.ModelAdmin):
    list_display = ("weather_id", "city", "date", "temperature_avg", "humidity", "solar_index", "source")
    list_filter = ("city", "source")


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ("forecast_id", "city", "forecast_time", "temp_c", "humidity", "wind_speed", "weather_main")
    list_filter = ("city", "weather_main", "source")
    ordering = ("-forecast_time",)