from django.db import models
from django.utils import timezone


class City(models.Model):                #المدن
    """
    Reference table for the selected cities (1..4).
    Source: final/selected_cities.csv
    """
    city_id = models.IntegerField(primary_key=True)  # 1..4 ثابت
    city_geo = models.CharField(max_length=50, unique=True)  # riyadh, jeddah, khobar, dammam
    city_name_ar = models.CharField(max_length=100)
    region_name_ar = models.CharField(max_length=100)

    class Meta:
        db_table = "cities"

    def __str__(self):
        return f"{self.city_geo} ({self.city_name_ar})"
    


class District(models.Model):
    district_id = models.AutoField(primary_key=True)

    district_name_ar = models.CharField(max_length=150)
    district_name_en = models.CharField(max_length=150, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="districts"
    )

    class Meta:
        db_table = "districts"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["district_name_ar"]),
        ]

    def __str__(self):
        return f"{self.district_name_ar} ({self.city.city_geo})"


class POICategory(models.Model):                       #فئات نقاط الاهتمام
    """
    Normalized category table.
    Source: final/poi_categories.parquet
    """
    category_id = models.IntegerField(primary_key=True)
    level1 = models.CharField(max_length=100)
    level2 = models.CharField(max_length=100, null=True, blank=True)
    level3 = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=50)

    class Meta:
        db_table = "poi_categories"
        indexes = [
            models.Index(fields=["level1"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return " > ".join([x for x in [self.level1, self.level2, self.level3] if x])


class POI(models.Model):                   #نقاط الاهتمام
    """
    Main POI table.
    Source: final/poi_selected.parquet
    """
    poi_id = models.CharField(max_length=120, primary_key=True)  # نصي (xmap / visitsaudi ...)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    phone = models.CharField(max_length=50, null=True, blank=True)
    website_domain = models.CharField(max_length=200, null=True, blank=True)

    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)

    traffic_score = models.FloatField(null=True, blank=True)
    time_spent = models.FloatField(null=True, blank=True)

    source = models.CharField(max_length=50, null=True, blank=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="pois")
    category = models.ForeignKey(POICategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="pois")

    class Meta:
        db_table = "pois"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["category"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return self.name


class Event(models.Model):                     #الفعاليات
    """
    Events for selected cities.
    Source: final/events_selected.parquet
    """
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    is_male_allowed = models.BooleanField(null=True, blank=True)
    is_female_allowed = models.BooleanField(null=True, blank=True)
    is_family_allowed = models.BooleanField(null=True, blank=True)

   
    source = models.CharField(max_length=50, null=True, blank=True)

    category = models.ForeignKey(
    "core_data.POICategory",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="events")

    



        
    @property
    def event_mode(self):
        today = timezone.now().date()
        if self.start_date and self.end_date:
            if self.start_date <= today <= self.end_date:
                return "IsActive"
        return "IsExpired"    



    class Meta:
        db_table = "events"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["start_date"]),
        ]

    def __str__(self):
        return self.name






class WeatherContext(models.Model):                  #السياق الجوي
    """
    Weather context (Solar + later OpenWeather snapshots).
    Source: final/weather_selected.parquet
    """
    weather_id = models.AutoField(primary_key=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="weather_records")
    date = models.DateField()

    temperature_avg = models.FloatField(null=True, blank=True)
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)

    weather_condition = models.CharField(max_length=100, null=True, blank=True)

    solar_index = models.FloatField(null=True, blank=True)  # من solar dataset
    source = models.CharField(max_length=50, default="solar")  # solar/openweather

    class Meta:
        db_table = "weather_context"
        unique_together = ("city", "date")
        indexes = [
            models.Index(fields=["city", "date"]),
        ]

    def __str__(self):
        return f"{self.city.city_geo} - {self.date}"
    





class WeatherForecast(models.Model):
    """
    OpenWeather forecast (every 3 hours) for selected cities.
    Source: final/weather_forecast_selected.parquet
    """

    forecast_id = models.AutoField(primary_key=True)

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="forecasts"
    )

    forecast_time = models.DateTimeField()

    temp_c = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)

    weather_main = models.CharField(max_length=50, null=True, blank=True)
    weather_desc = models.CharField(max_length=100, null=True, blank=True)

    source = models.CharField(max_length=30, default="openweather")

    class Meta:
        db_table = "weather_forecasts"
        unique_together = ("city", "forecast_time")
        indexes = [
            models.Index(fields=["city", "forecast_time"]),
        ]

    def __str__(self):
        return f"{self.city.city_geo} @ {self.forecast_time}"


