from django.conf.urls import url

from rest_framework_nested import routers

from .views import (
    StoriesViewSet, StoryLinesViewSet,
    UserBlock
)


story_router = routers.SimpleRouter()
story_router.register(r'story', StoriesViewSet, base_name='story')

storylines_router = routers.NestedSimpleRouter(
    story_router, r'story', lookup='story'
)
storylines_router.register(
    r'storylines', StoryLinesViewSet, base_name='storylines'
)

urlpatterns = [
    url(
        r'^story/(?P<pk>[0-9]+)/block/(?P<user_pk>[0-9]+)/',
        UserBlock.as_view(),
        name='block'
    )
]
urlpatterns += story_router.urls
urlpatterns += storylines_router.urls
