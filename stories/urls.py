from django.conf.urls import url

from rest_framework_nested import routers

from .views import (
    StoriesViewSet, PersonalStoryList, TrendingStoryList, StoryLinesViewSet,
    StoryVote, StoryUnvote,
    UserBlock, UserUnblock
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
        r'^story/personal/', PersonalStoryList.as_view(), name='personal'
    ),
    url(
        r'^story/trending/', TrendingStoryList.as_view(), name='trending'
    ),
    url(
        r'^story/(?P<pk>[0-9]+)/vote/', StoryVote.as_view(), name='vote'
    ),
    url(
        r'^story/(?P<pk>[0-9]+)/unvote/', StoryUnvote.as_view(), name='unvote'
    ),
    url(
        r'^story/(?P<pk>[0-9]+)/block/(?P<user_pk>[0-9]+)/',
        UserBlock.as_view(),
        name='block'
    ),
    url(
        r'^story/(?P<pk>[0-9]+)/unblock/(?P<user_pk>[0-9]+)/',
        UserUnblock.as_view(),
        name='unblock'
    )
]

urlpatterns += story_router.urls
urlpatterns += storylines_router.urls
