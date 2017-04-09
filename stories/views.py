from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import StorySerializer, StoryLineSerializer
from .models import Story, StoryLine
from .permissions import (
    IsAuthor, IsNotBlacklisted,
    IsNotLastStoryLineAuthor, IsNotFullOfStoryLines
)


class StoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
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

        resp_data = serializer.data
        resp_data['have_voted'] = story.votes.exists(request.user.pk)

        return Response(
            resp_data,
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


class PersonalStoryList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StorySerializer

    def get(self, request):
        stories = Story.objects.filter(author=request.user.author)
        serializer = self.serializer_class(stories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TrendingStoryList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StorySerializer

    def get(self, request):
        stories = Story.objects.order_by('-num_vote_up', '-posted_on')[:10]
        serializer = self.serializer_class(stories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StoryLinesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (
            IsAuthenticated, IsNotBlacklisted,
            IsNotLastStoryLineAuthor, IsNotFullOfStoryLines
        ),
        'destroy': (IsAuthenticated, IsAuthor),
    }
    serializer_class = StoryLineSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

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

        resp_data = serializer.data
        resp_data['story_id'] = int(story.id)

        return Response(
            resp_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def destroy(self, request, story_pk=None, pk=None):
        story = get_object_or_404(Story, id=story_pk)
        story_line = get_object_or_404(story.storyline_set, id=pk)
        self.check_object_permissions(request, story)

        story_line.delete()

        return Response(
            {'message': 'Story line successfuly deleted.'},
            status=status.HTTP_200_OK
        )


class StoryVotingView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotBlacklisted)

    def perform_action(self, user_id, story):
        raise NotImplementedError()

    def update(self, request, pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)
        self.check_object_permissions(request, story)

        self.perform_action(request.user.id, story)

        return Response(
            {'num_vote_up': story.votes.count()},
            status=status.HTTP_200_OK
        )


class StoryVote(StoryVotingView):
    def perform_action(self, user_id, story):
        story.votes.up(user_id)


class StoryUnvote(StoryVotingView):
    def perform_action(self, user_id, story):
        story.votes.delete(user_id)


class UserBlockingView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthor)

    err_msg_format = 'User {} is {}.'
    resp_msg_format = 'User {} has been successfully {}.'

    def get_error_message(self, user):
        raise NotImplementedError()

    def get_response_message(self, user):
        raise NotImplementedError()

    def can_perform_action(self, user, story):
        raise NotImplementedError()

    def get_users_queryset(self, story=None):
        raise NotImplementedError()

    def perform_action(self, user, story):
        raise NotImplementedError()

    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)

        user = get_object_or_404(self.get_users_queryset(story), id=user_pk)

        self.check_object_permissions(request, story)

        if not self.can_perform_action(user, story):
            return Response(
                {'message': self.get_error_message(user)},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_action(user, story)

        return Response(
            {'message': self.get_response_message(user)},
            status=status.HTTP_200_OK
        )


class UserUnblock(UserBlockingView):
    def get_error_message(self, user):
        return self.err_msg_format.format(user, 'not blocked yet')

    def get_response_message(self, user):
        return self.resp_msg_format.format(user, 'unblocked')

    def can_perform_action(self, user, story):
        return user in story.blacklist.all()

    def get_users_queryset(self, story=None):
        return User.objects.all()

    def perform_action(self, user, story):
        story.blacklist.remove(user)


class UserBlock(UserUnblock):
    def get_error_message(self, user):
        return self.err_msg_format.format(user, 'already blocked')

    def get_response_message(self, user):
        return self.resp_msg_format.format(user, 'blocked')

    def can_perform_action(self, user, story):
        return not super().can_perform_action(user, story)

    def get_users_queryset(self, story=None):
        return super().get_users_queryset(story=story).exclude(id=story.author.user.id)

    def perform_action(self, user, story):
        story.blacklist.add(user)
