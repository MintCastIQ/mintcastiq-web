# urls.py
from rest_framework import routers
from .views import DimCardViewSet

router = routers.DefaultRouter()
router.register(r'dimcards', DimCardViewSet)

urlpatterns = router.urls
