from rest_framework import serializers

from users.serializers import AuthorSerializer
from .models import Story, StoryLine


class StoryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryLine
        fields = ('id', 'content', 'posted_on')


class StorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=100)
    author = AuthorSerializer(read_only=True)
    storyline_set = StoryLineSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ('id', 'title', 'author', 'posted_on', 'storyline_set')

    def create(self, validated_data):
        request = self.context['request']
        author = request.user.author

        return Story.objects.create(author=author, **validated_data)
