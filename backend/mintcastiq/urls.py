from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import DimCardViewSet

router = routers.DefaultRouter()
# router.register(r'dimcards', DimCardViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),  # include DRF routes
]

