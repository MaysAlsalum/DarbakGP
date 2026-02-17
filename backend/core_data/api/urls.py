from rest_framework.routers import DefaultRouter
from .views import (
    CityViewSet,
    POICategoryViewSet,
    POIViewSet,
    POIMapViewSet,
    EventViewSet,
    WeatherForecastViewSet,
)

router = DefaultRouter()
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"poi-categories", POICategoryViewSet, basename="poi-categories")
router.register(r"pois", POIViewSet, basename="pois")
router.register(r"events", EventViewSet, basename="events")
router.register(r"weather-forecast", WeatherForecastViewSet, basename="weather-forecast")
router.register(r"pois-map", POIMapViewSet, basename="pois-map")
urlpatterns = router.urls