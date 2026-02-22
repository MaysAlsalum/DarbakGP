from django.urls import path
from .views import CategoryChoicesAPIView,CategoryLevel1APIView, CategoryLevel2APIView, CategoryLevel3APIView, CategoryTreeAPIView, UserPreferencesAPIView

urlpatterns = [
    path("categories/choices/", CategoryChoicesAPIView.as_view(), name="category-choices"),
    path("user/preferences/", UserPreferencesAPIView.as_view(), name="user-preferences"),
    path("categories/tree/", CategoryTreeAPIView.as_view(), name="category-tree"),
    path("categories/level1/", CategoryLevel1APIView.as_view()),
    path("categories/level2/", CategoryLevel2APIView.as_view()),
    path("categories/level3/", CategoryLevel3APIView.as_view()),
    
]
