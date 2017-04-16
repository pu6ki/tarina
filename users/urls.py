from django.conf.urls import url

from .views import UserRegistration, UserLogin, AuthorProfile


app_name = 'users'

urlpatterns = [
    url(r'^register/', UserRegistration.as_view(), name='register'),
    url(r'^login/', UserLogin.as_view(), name='login'),
    url(r'^profile/(?P<user_pk>[0-9]+)/', AuthorProfile.as_view(), name='profile')
]
