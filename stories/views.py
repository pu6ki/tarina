from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import StorySerializer, StoryLineSerializer
from .models import Story, StoryLine
from .permissions import IsAuthor, IsNotBlacklisted, IsBlacklisted


class StoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsNotBlacklisted),
        'create': (IsAuthenticated,),
        'destroy': (IsAuthenticated, IsAuthor),
    }
    serializer_class = StorySerializer
    queryset = Story.objects.all()

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

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

    def destroy(self, request, pk=None):
        story = get_object_or_404(Story, id=pk)
        self.check_object_permissions(request, story)

        story.delete()

        return Response(
            {'message': 'Story successfuly deleted.'},
            status=status.HTTP_200_OK
        )


class UserBlockingView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)

    def get_response_message(self, user):
        return 'User {} has been successfuly {}.'.format(
            user,
            'blocked' if self.get_view_name().endswith('Block') else 'unblocked'
        )

    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        raise NotImplementedError()


class UserBlock(UserBlockingView):
    permission_classes = (IsAuthenticated, IsAuthor, IsNotBlacklisted)

    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)

        users = User.objects.exclude(id=story.author.user.pk)
        user = get_object_or_404(users, id=user_pk)

        request.user = user
        self.check_object_permissions(request, story)

        story.blacklist.remove(user)

        return Response(
            {'message': self.get_response_message(user)},
            status=status.HTTP_200_OK
        )


class UserUnblock(UserBlockingView):
    permission_classes = (IsAuthenticated, IsAuthor, IsBlacklisted)

    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)

        users = User.objects.exclude(id=story.author.user.pk)
        user = get_object_or_404(users, id=user_pk)

        request.user = user
        self.check_object_permissions(request, story)

        story.blacklist.add(user)

        return Response(
            {'message': self.get_response_message(user)},
            status=status.HTTP_200_OK
        )


class StoryLinesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StoryLineSerializer

    def list(self, request, story_pk=None):
        story = get_object_or_404(Story, id=story_pk)
        self.check_object_permissions(request, story)

        storylines = StoryLine.objects.filter(story=story)
        serializer = self.serializer_class(storylines, many=True)

        headers = self.get_success_headers(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def retrieve(self, request, story_pk=None, pk=None):
        story = get_object_or_404(Story, id=story_pk)
        self.check_object_permissions(request, story)

        storyline = get_object_or_404(story.storyline_set, id=pk)
        serializer = self.serializer_class(storyline)

        headers = self.get_success_headers(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def create(self, request, story_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=story_pk)
        self.check_object_permissions(request, story)

        context = {'request': request, 'story': story}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
