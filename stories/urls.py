from rest_framework_nested import routers

from .views import StoriesViewSet, StoryLinesViewSet


story_router = routers.SimpleRouter()
story_router.register(r'story', StoriesViewSet, base_name='story')

storylines_router = routers.NestedSimpleRouter(
    story_router, r'story', lookup='story'
)
storylines_router.register(
    r'storylines', StoryLinesViewSet, base_name='storylines'
)

urlpatterns = story_router.urls
urlpatterns += storylines_router.urls
