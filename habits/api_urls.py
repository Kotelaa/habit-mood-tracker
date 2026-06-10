from rest_framework.routers import DefaultRouter

from .api_views import HabitViewSet, MoodViewSet

router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habit')
router.register('mood', MoodViewSet, basename='mood')
urlpatterns = router.urls

