from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import Author
from .models import Story, StoryLine


class StoriesViewSetTests(APITestCase):
    def setUp(self):
        self.list_view_name = 'stories:story-list'
        self.detail_view_name = 'stories:story-detail'

        self.user = User.objects.create(
            username='Litelight',
            password='hasanypairnowrunnin',
            first_name='Kndrck',
            last_name='Lmr'
        )
        self.author = Author.objects.create(user=self.user)
        self.story = Story.objects.create(title='Test!',author=self.author)

        self.request_body = {'title': 'Drama goes down.'}
        self.http_401_message = 'Authentication credentials were not provided.'
        self.http_403_message = 'You do not have permission to perform this action.'
        self.http_404_message = 'Not found.'

    def test_story_list_with_unauthorized_user(self):
        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.data['detail'], self.http_401_message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_list_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(self.story.title, response.data[0]['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_unauthorized_user(self):
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], self.http_401_message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_detail_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(self.story.title, response.data['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id + 1}))

        self.assertEqual(response.data['detail'], self.http_404_message)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_story_creation_with_unauthorized_user(self):
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.data['detail'], self.http_401_message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_creation_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_story_deletion_with_unauthorized_user(self):
        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], self.http_401_message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        self.new_user = User.objects.create(username='joey', password='trigger123')
        self.story.author = Author.objects.create(user=self.new_user)
        self.story.save()

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], self.http_403_message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_story_deletion_with_valid_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['message'], 'Story successfully deleted.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)