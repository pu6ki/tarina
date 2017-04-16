from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    AuthorSerializer
)
from .models import Author


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(
            {'message': 'You successfully registered. You can login now.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'message': 'Unable to login with the provided credentials.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = Token.objects.get(user=user)
        headers = self.get_success_headers(serializer)

        resp_data = {
            'token': token.key,
            'id': user.id,
            'username': user.username
        }

        return Response(resp_data, status=status.HTTP_200_OK, headers=headers)


class AuthorProfile(generics.RetrieveUpdateAPIView):
    serializer_class = AuthorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, user_pk=None, *args, **kwargs):
        author = get_object_or_404(Author, user__id=user_pk)

        serializer = self.serializer_class(author)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, user_pk=None):
        author = get_object_or_404(Author, user__id=user_pk)
        News.objects.create()

        serializer = self.serializer_class(author, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
