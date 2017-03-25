# from django.shortcuts import get_object_or_404

from rest_framework import viewsets
# from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import StorySerializer
from .models import Story


class StoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StorySerializer
    queryset = Story.objects.all()
