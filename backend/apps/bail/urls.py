from rest_framework.routers import DefaultRouter
from .views import BailRuleViewSet

router = DefaultRouter()
router.register(r'', BailRuleViewSet, basename='bail')

urlpatterns = router.urls
