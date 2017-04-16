from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import Author
from .models import Story, StoryLine


HTTP_MESSAGES = {
    401: 'Authentication credentials were not provided.',
    403: 'You do not have permission to perform this action.',
    404: 'Not found.'
}


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
        self.story = Story.objects.create(title='Test!', author=self.author)

        self.request_body = {'title': 'Drama goes down.'}

    def test_story_list_with_unauthorized_user(self):
        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_list_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(self.story.title, response.data[0]['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_unauthorized_user(self):
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_detail_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(self.story.title, response.data['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id + 1}))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_story_creation_with_unauthorized_user(self):
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_story_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)

        self.request_body['title'] = 'ya'
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.data['title'], ['Ensure this field has at least 3 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)

        self.request_body['title'] = 'test' * 30
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.data['title'], ['Ensure this field has no more than 100 characters.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_creation_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_story_deletion_with_unauthorized_user(self):
        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        self.new_user = User.objects.create(username='joey', password='trigger123')
        self.story.author = Author.objects.create(user=self.new_user)
        self.story.save()

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_story_deletion_with_valid_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(response.data['message'], 'Story successfully deleted.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CategoryStoryListViewTests(APITestCase):
    def setUp(self):
        self.view_name = 'stories:category-list'

        self.user = User.objects.create(
            username='Litelight',
            password='hasanypairnowrunnin',
            first_name='Kndrck',
            last_name='Lmr'
        )
        self.author = Author.objects.create(user=self.user)
        self.story1 = Story.objects.create(title='Test!', author=self.author)
        self.story2 = Story.objects.create(title='Feel the buzz!', author=self.author)

    def test_category_list_with_unauthorized_user(self):
        response = self.client.get(reverse(self.view_name, kwargs={'category': 'test'}))

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[response.status_code])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_list_with_invalid_category(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.view_name, kwargs={'category': 'test'}))

        self.assertEqual(response.data['message'], 'Invalid category.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_personal_category_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.view_name, kwargs={'category': 'personal'}))

        self.assertEqual(response.data[0]['title'], self.story2.title)
        self.assertEqual(response.data[1]['title'], self.story1.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trending_category_list(self):
        self.client.force_authenticate(user=self.user)

        self.story1.num_vote_up += 3
        self.story2.num_vote_up += 1
        self.story1.save()
        self.story2.save()
        response = self.client.get(reverse(self.view_name, kwargs={'category': 'trending'}))

        self.assertEqual(response.data[0]['title'], self.story1.title)
        self.assertEqual(response.data[1]['title'], self.story2.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StoryLinesViewSetTests(APITestCase):
    def setUp(self):
        pass

    def test_story_line_list_with_unauthorized_user(self):
        pass

    def test_story_line_list_with_invalid_story_id(self):
        pass

    def test_story_line_list_with_valid_story_id(self):
        pass

    def test_story_line_detail_with_unauthorized_user(self):
        pass

    def test_story_line_detail_with_invalid_story_id(self):
        pass

    # Well...
    def test_story_line_detail_with_valid_story_id_and_invalid_story_line_id(self):
        pass

    def test_story_line_detail_with_valid_ids(self):
        pass

    def test_story_line_creation_with_unauthorized_user(self):
        pass
    
    def test_story_line_creation_with_invalid_story_id(self):
        pass
    
    def test_story_line_creation_with_too_short_content(self):
        pass
    
    def test_story_line_creation_with_too_long_content(self):
        pass

    def test_story_line_creation_with_blacklisted_author(self):
        pass
    
    def test_story_line_creation_when_request_user_is_last_author(self):
        pass

    def test_story_line_creation_when_story_is_full_of_story_lines(self):
        pass

    def test_story_line_creation_with_valid_data(self):
        pass

    def test_story_line_deletion_with_unauthorized_user(self):
        pass

    def test_story_line_deletion_with_invalid_story_id(self):
        pass

    def test_story_line_deletion_with_valid_story_id_and_invalid_story_line_id(self):
        pass
    
    def test_story_line_deletion_of_another_user(self):
        pass

    def test_story_line_deletion_with_valid_user(self):
        pass
