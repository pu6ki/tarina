from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import Author


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3,
        max_length=25,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this username already exists.'
            )
        ]
    )
    first_name = serializers.CharField(min_length=3, max_length=25)
    last_name = serializers.CharField(min_length=3, max_length=25)
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        Token.objects.create(user=user)
        Author.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    profile_image = serializers.URLField()

    class Meta:
        model = Author
        fields = ('user', 'profile_image')
