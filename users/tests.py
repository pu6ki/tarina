from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Author


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_view = reverse('users:register')
        self.login_view = reverse('users:login')

        self.username = 'K-Dot'
        self.password = 'wegonbealright'
        self.login_request_body = {
            'username': self.username,
            'password': self.password
        }
        self.register_request_body = self.login_request_body
        self.register_request_body['first_name'] = 'Kendrick'
        self.register_request_body['last_name'] = 'Lamar'

    def test_registration_with_existing_username(self):
        User.objects.create_user(username='K-Dot', email=None, password='theblackertheberry')
        response = self.client.post(self.register_view, self.register_request_body)
        
        self.assertEqual(
            response.data['username'], ['User with this username already exists.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_with_too_short_password(self):
        self.register_request_body['password'] = '123'
        response = self.client.post(self.register_view, self.register_request_body)
        
        self.assertEqual(
            response.data['password'], ['Ensure this field has at least 6 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registration_with_valid_credentials(self):
        response = self.client.post(self.register_view, self.register_request_body)

        self.assertEqual(
            response.data['message'], 'You successfully registered. You can login now.'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.register_view, self.register_request_body)

        self.assertEqual(
            response.data['message'], 'You successfully registered. You can login now.'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.login_request_body['username'] = 'Logic'
        response = self.client.post(self.login_view, self.login_request_body)

        self.assertEqual(response.data['message'], 'Unable to login with the provided credentials.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_with_valid_credentials(self):
        response = self.client.post(self.register_view, self.register_request_body)

        self.assertEqual(
            response.data['message'], 'You successfully registered. You can login now.'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.login_view, self.login_request_body)

        self.assertEqual(response.data['token'], Token.objects.get(user__username=self.username).key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorProfileTests(APITestCase):
    def setUp(self):
        self.view_name = 'users:profile'

        self.user = User.objects.create(
            username='JoeyBD$',
            password='devastated',
            first_name='Joey',
            last_name='Bada$$'
        )
        self.author = Author.objects.create(user=self.user)

    def test_profile_with_unauthorized_user(self):
        response = self.client.get(reverse(self.view_name, kwargs={'user_pk': self.user.id}))

        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.view_name, kwargs={'user_pk': self.user.id}))

        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        

    def test_profile_with_invalid_user_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.view_name, kwargs={'user_pk': self.user.id + 1}))

        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
