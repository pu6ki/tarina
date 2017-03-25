from rest_framework import serializers

from users.serializers import AuthorSerializer
from .models import Story


class StorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=3)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Story
        fields = ('id', 'title', 'author', 'posted_on')
