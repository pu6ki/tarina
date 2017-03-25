from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import StorySerializer
from .models import Story


class StoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StorySerializer
    queryset = Story.objects.all()

    def retrieve(self, request, pk=None):
        story = get_object_or_404(Story, id=pk)
        self.check_object_permissions(request, story)

        serializer = self.serializer_class(story)

        headers = self.get_success_headers(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
