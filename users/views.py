from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(
            {'message': 'You successfully registered. You can log in now.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
