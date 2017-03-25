from rest_framework.routers import SimpleRouter

from .views import StoriesViewSet


story_router = SimpleRouter()
story_router.register(r'story', StoriesViewSet, base_name='story')

urlpatterns = story_router.urls
