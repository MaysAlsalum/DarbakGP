from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response
from core_data.models import City, POICategory, POI, Event, WeatherForecast
from .serializers import (
    CitySerializer,
    POICategorySerializer,
    POIMapSerializer,
    POISerializer,
    EventSerializer,
    WeatherForecastSerializer,
)


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all().order_by("city_id")
    serializer_class = CitySerializer


class POICategoryViewSet(ReadOnlyModelViewSet):
    queryset = POICategory.objects.all().order_by("category_id")
    serializer_class = POICategorySerializer


class POIViewSet(ReadOnlyModelViewSet):
    queryset = POI.objects.select_related("city", "category").all()
    serializer_class = POISerializer



    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["city__city_id", "category__category_id", "source"]
    search_fields = ["name", "address"]
    ordering_fields = ["rating", "rating_count", "traffic_score", "time_spent"]
    ordering = ["-rating"]

    # فلترة بالـ query params
    def get_queryset(self):
        qs = super().get_queryset()
        city_id = self.request.query_params.get("city_id")
        category_id = self.request.query_params.get("category_id")

        if city_id:
            qs = qs.filter(city__city_id=int(city_id))

        if category_id:
            qs = qs.filter(category__category_id=int(category_id))

        return qs
    
    @action(detail=False, methods=["get"], url_path="smart-top")
    def smart_top(self, request):
        city_id = request.query_params.get("city_id")
        limit = int(request.query_params.get("limit", 20))

        qs = self.get_queryset()

        if city_id:
            qs = qs.filter(city__city_id=int(city_id))

        # نحسب score مركب
        qs = qs.annotate(
            smart_score=ExpressionWrapper(
                Coalesce(F("rating"), 0.0) * 0.5 +
                Coalesce(F("traffic_score"), 0.0) * 0.3 +
                Coalesce(F("rating_count"), 0.0) * 0.0005,
                output_field=FloatField()
            )
        ).order_by("-smart_score")[:limit]

        data = POIMapSerializer(qs, many=True).data
        return Response(data)


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.select_related("city").all()
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        city_id = self.request.query_params.get("city_id")
        if city_id:
            qs = qs.filter(city__city_id=int(city_id))
        return qs


class WeatherForecastViewSet(ReadOnlyModelViewSet):
    queryset = WeatherForecast.objects.select_related("city").all()
    serializer_class = WeatherForecastSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        city_id = self.request.query_params.get("city_id")
        if city_id:
            qs = qs.filter(city__city_id=int(city_id))
        return qs.order_by("forecast_time")
    







class POIMapViewSet(ReadOnlyModelViewSet):
    serializer_class = POIMapSerializer

    def get_queryset(self):
        qs = POI.objects.select_related("city", "category").all()

        city_id = self.request.query_params.get("city_id")
        category_id = self.request.query_params.get("category_id")

        if city_id:
            qs = qs.filter(city__city_id=int(city_id))
        if category_id:
            qs = qs.filter(category__category_id=int(category_id))

        # للخريطة غالبًا ما نحتاج ترتيب معقد
        return qs.only("poi_id", "name", "latitude", "longitude", "rating", "city_id", "category_id")