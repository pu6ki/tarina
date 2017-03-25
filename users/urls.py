from django.conf.urls import url

from .views import UserRegistration


urlpatterns = [
    url(r'^register/', UserRegistration.as_view(), name='register'),
]