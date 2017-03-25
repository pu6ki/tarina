from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import StorySerializer, StoryLineSerializer
from .models import Story, StoryLine
from .permissions import IsAuthor, IsNotBlacklisted


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
        stories = Story.objects.order_by('num_vote_up', '-posted_on')[:10]
        serializer = self.serializer_class(stories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StoryLinesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsNotBlacklisted),
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

        story_lines = StoryLine.objects.filter(story=story)
        user_story_lines = story_lines.filter(author=request.user.author)

        if story_lines:
            msg = ''

            if story_lines.last() == user_story_lines.last():
                msg = 'You are not allowed to add two consecutive story lines.'
            elif story_lines.filter(content=request.data['content']):
                msg = 'Identical story line already exists.'
            elif len(story_lines) == 30:
                msg = 'Max number of stories reached.'

            if msg:
                return Response(
                    {'message': msg},
                    status=status.HTTP_403_FORBIDDEN
                )

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


class StoryVoting(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotBlacklisted)

    def get_error_message(self):
        unvote_msg = 'You haven\'t voted for this story yet.'
        vote_msg = 'You have already voted for this story.'

        return unvote_msg if self.get_view_name().endswith('Unvote') else vote_msg

    def update(self, request, pk=None, *args, **kwargs):
        raise NotImplementedError()


class StoryVote(StoryVoting):
    def update(self, request, pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)
        self.check_object_permissions(request, story)

        user_id = request.user.id

        if story.votes.exists(user_id):
            return Response(
                {'message': self.get_error_message()},
                status=status.HTTP_400_BAD_REQUEST
            )

        story.votes.up(user_id)

        return Response(
            {'num_vote_up': story.votes.count()},
            status=status.HTTP_200_OK
        )


class StoryUnvote(StoryVoting):
    def update(self, request, pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)
        self.check_object_permissions(request, story)

        user_id = request.user.id

        if not story.votes.exists(user_id):
            return Response(
                {'message': self.get_error_message()},
                status=status.HTTP_400_BAD_REQUEST
            )

        story.votes.delete(user_id)

        return Response(
            {'num_vote_up': story.votes.count()},
            status=status.HTTP_200_OK
        )


class UserBlockingView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthor)

    def get_response_message(self, user):
        return 'User {} has been successfuly {}.'.format(
            user,
            'blocked' if self.get_view_name().endswith('Block') else 'unblocked'
        )

    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        raise NotImplementedError()


class UserBlock(UserBlockingView):
    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)

        users = User.objects.exclude(id=story.author.user.pk)
        user = get_object_or_404(users, id=user_pk)

        self.check_object_permissions(request, story)

        if user in story.blacklist.all():
            return Response(
                {'message': 'User is already blocked.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        story.blacklist.add(user)

        return Response(
            {'message': self.get_response_message(user)},
            status=status.HTTP_200_OK
        )


class UserUnblock(UserBlockingView):
    def update(self, request, pk=None, user_pk=None, *args, **kwargs):
        story = get_object_or_404(Story, id=pk)
        user = get_object_or_404(User, id=user_pk)

        self.check_object_permissions(request, story)

        if user not in story.blacklist.all():
            return Response(
                {'message': 'User is not blocked yet.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        story.blacklist.remove(user)

        return Response(
            {'message': self.get_response_message(user)},
            status=status.HTTP_200_OK
        )
