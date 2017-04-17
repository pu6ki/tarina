from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Author
from .models import Story, StoryLine
from .permissions import IsNotBlacklisted, IsNotLastStoryLineAuthor


HTTP_MESSAGES = {
    401: 'Authentication credentials were not provided.',
    403: {
        'default': 'You do not have permission to perform this action.',
        'blacklisted': IsNotBlacklisted().message,
        'last_author': IsNotLastStoryLineAuthor().message
    },
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

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_list_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.list_view_name))

        self.assertEqual(self.story.title, response.data[0]['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_unauthorized_user(self):
        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_detail_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        self.assertEqual(self.story.title, response.data['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_detail_with_invalid_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse(self.detail_view_name, kwargs={'pk': self.story.id + 1}))

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_creation_with_unauthorized_user(self):
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_creation_with_too_short_title(self):
        self.client.force_authenticate(user=self.user)

        self.request_body['title'] = 'ya'
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(
            response.data['title'], ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_creation_with_too_long_title(self):
        self.client.force_authenticate(user=self.user)

        self.request_body['title'] = 'test' * 30
        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(
            response.data['title'], ['Ensure this field has no more than 100 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_creation_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse(self.list_view_name), self.request_body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_story_deletion_with_unauthorized_user(self):
        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_deletion_of_another_user(self):
        self.client.force_authenticate(user=self.user)

        new_user = User.objects.create(username='joey', password='trigger123')
        self.story.author = Author.objects.create(user=new_user)
        self.story.save()

        response = self.client.delete(reverse(self.detail_view_name, kwargs={'pk': self.story.id}))

        status_code = response.status_code

        self.assertEqual(
            response.data['detail'], HTTP_MESSAGES[status_code]['default']
        )
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)

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

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.list_view_name = 'stories:storylines-list'
        self.detail_view_name = 'stories:storylines-detail'

        self.user1 = User.objects.create(
            username='Avenue',
            password='javafordummies',
            first_name='Doomer',
            last_name='Test'
        )
        self.user2 = User.objects.create(
            username='J. Cole',
            password='2014FHD',
            first_name='Jermaine',
            last_name='Cole'
        )
        self.author1 = Author.objects.create(user=self.user1)
        self.author2 = Author.objects.create(user=self.user2)

        self.story = Story.objects.create(title='Test Story', author=self.author1)
        self.storyline1 = StoryLine.objects.create(
            content='Beautiful!',
            story=self.story,
            author=self.author1
        )
        self.storyline2 = StoryLine.objects.create(
            content='4 YOUR EYEZ ONLY',
            story=self.story,
            author=self.author2
        )

    def test_story_line_list_with_unauthorized_user(self):
        response = self.client.get(
            reverse(
                self.list_view_name, kwargs={'story_pk': self.story.id}
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_line_list_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.list_view_name, kwargs={'story_pk': self.story.id + 1}
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_list_with_valid_story_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.list_view_name, kwargs={'story_pk': self.story.id}
            )
        )

        self.assertEqual(response.data[0]['content'], self.storyline1.content)
        self.assertEqual(response.data[1]['content'], self.storyline2.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_line_detail_with_unauthorized_user(self):
        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline1.id
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_line_detail_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id + 1,
                    'pk': self.storyline1.id
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_detail_with_valid_story_id_and_invalid_story_line_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline2.id + 1
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_detail_with_valid_ids(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            reverse(
                self.detail_view_name, kwargs={'story_pk': self.story.id, 'pk': self.storyline1.id}
            )
        )

        self.assertEqual(response.data['content'], self.storyline1.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_line_creation_with_unauthorized_user(self):
        response = self.client.post(
            reverse(
                self.list_view_name,
                kwargs={'story_pk': self.story.id}
            ),
            data={'content': 'All eyez on me.'}
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_line_creation_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id + 1}),
            data={'content': 'All eyez on me.'}
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_creation_with_too_short_content(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id}),
            data={'content': 'ye'}
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has at least 3 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_line_creation_with_too_long_content(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id}),
            data={'content': 'fire' * 100}
        )

        self.assertEqual(
            response.data['content'], ['Ensure this field has no more than 250 characters.']
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_story_line_creation_with_blacklisted_author(self):
        self.client.force_authenticate(user=self.user1)

        self.story.blacklist.add(self.user1)
        self.story.save()

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id}),
            data={'content': 'for your eyez only!'}
        )

        status_code = response.status_code

        self.assertEqual(
            response.data['detail'], HTTP_MESSAGES[status_code]['blacklisted']
        )
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)

    def test_story_line_creation_when_request_user_is_last_author(self):
        self.client.force_authenticate(user=self.user2)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id}),
            data={'content': 'for your eyez only!'}
        )

        status_code = response.status_code

        self.assertEqual(
            response.data['detail'], HTTP_MESSAGES[status_code]['last_author']
        )
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)

    def test_story_line_creation_when_story_is_full_of_story_lines(self):
        pass

    def test_story_line_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse(self.list_view_name, kwargs={'story_pk': self.story.id}),
            data={'content': 'for your eyez only!'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_story_line_deletion_with_unauthorized_user(self):
        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline1.id
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_story_line_deletion_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id + 1,
                    'pk': self.storyline1.id
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_deletion_with_valid_story_id_and_invalid_story_line_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline2.id + 1
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_story_line_deletion_when_request_user_is_not_story_author(self):
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline2.id
                }
            )
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code]['default'])
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)

    def test_story_line_deletion_with_valid_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            reverse(
                self.detail_view_name,
                kwargs={
                    'story_pk': self.story.id,
                    'pk': self.storyline2.id
                }
            )
        )

        self.assertEqual(response.data['message'], 'Story line successfully deleted.')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StoryVotingTests(APITestCase):
    def setUp(self):
        self.vote_view_name = 'stories:vote'
        self.unvote_view_name = 'stories:unvote'

        self.user = User.objects.create(
            username='DAMN',
            password='straightouttacompton',
            first_name='Kendrick',
            last_name='Lamar'
        )
        self.blocked_user = User.objects.create(
            username='Millenium',
            password='alwaysonyourmind',
            first_name='Lifeline',
            last_name='Ontheline'
        )
        self.author = Author.objects.create(user=self.user)
        self.story = Story.objects.create(title='Church', author=self.author)
        self.story.blacklist.add(self.blocked_user)
        self.story.save()

    def test_voting_with_unauthorized_user(self):
        response = self.client.put(
            reverse(self.vote_view_name, kwargs={'pk': self.story.id})
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_voting_when_user_is_blocked(self):
        self.client.force_authenticate(user=self.blocked_user)

        response = self.client.put(
            reverse(self.vote_view_name, kwargs={'pk': self.story.id})
        )

        status_code = response.status_code

        self.assertEqual(
            response.data['detail'], HTTP_MESSAGES[status_code]['blacklisted']
        )
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)

    def test_voting_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.vote_view_name, kwargs={'pk': self.story.id + 1})
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)

    def test_voting_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.vote_view_name, kwargs={'pk': self.story.id})
        )

        status_code = response.status_code

        self.assertEqual(response.data['num_vote_up'], 1)
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_unvoting_with_unauthorized_user(self):
        response = self.client.put(
            reverse(self.unvote_view_name, kwargs={'pk': self.story.id})
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unvoting_with_invalid_story_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.unvote_view_name, kwargs={'pk': self.story.id + 1})
        )

        status_code = response.status_code

        self.assertEqual(response.data['detail'], HTTP_MESSAGES[status_code])
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)


    def test_unvoting_with_authorized_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse(self.vote_view_name, kwargs={'pk': self.story.id})
        )

        self.assertEqual(response.data['num_vote_up'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse(self.unvote_view_name, kwargs={'pk': self.story.id})
        )

        self.assertEqual(response.data['num_vote_up'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserBlockingTests(APITestCase):
    def setUp(self):
        pass

    def test_user_block_with_unauthorized_user(self):
        pass

    def test_user_block_when_request_user_is_not_author(self):
        pass

    def test_user_block_with_invalid_user_id(self):
        pass

    def test_user_block_when_user_is_already_blocked(self):
        pass

    def test_user_block_with_same_user(self):
        pass

    def test_user_block_with_valid_unblocked_user(self):
        pass

    def test_user_unblock_with_unauthorized_user(self):
        pass

    def test_user_unblock_when_request_user_is_not_author(self):
        pass

    def test_user_unblock_with_invalid_user_id(self):
        pass

    def test_user_unblock_when_user_is_not_blocked_yet(self):
        pass

    def test_user_unblock_with_same_user(self):
        pass

    def test_user_unblock_with_valid_blocked_user(self):
        pass
