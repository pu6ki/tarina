from django.conf import settings

from rest_framework import permissions

from .models import StoryLine


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author.user


class IsNotBlacklisted(permissions.BasePermission):
    message = 'You are not allowed to contribute to this story anymore.'

    def has_object_permission(self, request, view, obj):
        return request.user not in obj.blacklist.all()


class IsNotLastStoryLineAuthor(permissions.BasePermission):
    message = 'You are not allowed to add two consecutive story lines.'

    def has_object_permission(self, request, view, obj):
        story_lines = StoryLine.objects.filter(story=obj)

        return story_lines.last() != story_lines.filter(author=request.user.author).last()


class IsNotFullOfStoryLines(permissions.BasePermission):
    message = 'Max number of story lines reached ({}).'.format(settings.MAX_STORYLINES)

    def has_object_permission(self, request, view, obj):
        story_lines = StoryLine.objects.filter(story=obj)

        return story_lines.count() < settings.MAX_STORYLINES
