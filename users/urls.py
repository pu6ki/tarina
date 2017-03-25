from django.conf.urls import url

from .views import UserRegistration, UserLogin


urlpatterns = [
    url(r'^register/', UserRegistration.as_view(), name='register'),
    url(r'^login/', UserLogin.as_view(), name='login')
]