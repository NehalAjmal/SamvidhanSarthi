from rest_framework.routers import DefaultRouter
from .views import RTIStepViewSet

router = DefaultRouter()
router.register(r'', RTIStepViewSet, basename='rti')

urlpatterns = router.urls
