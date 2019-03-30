import base64
import json

from django.contrib.auth.models import User
from rest_api.models import Post
from rest_framework.test import APITestCase
from django.urls import reverse


def get_user_id(token):
    payload = token.split('.')[1]
    payload_decode = base64.b64decode(payload)
    payload_dict = json.loads(payload_decode, encoding='UTF8')

    return payload_dict['user_id']


class UserAndPostTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mmitch',
            email='mmitch@email.com',
            password='1234'
        )
        self.user_data = {
            'username': self.user.username,
            'password': '1234'
        }

    def test_valid_signup(self):
        """ Register user with username=test_user."""
        data = {
            'email': 'test_user@gmail.com',
            'username': 'test_user',
            'password': '1234'
        }
        response = self.client.post(reverse('register'), data, format='json')

        user = User.objects.get(username='test_user')

        self.assertEqual(user.username, data['username'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'user_create'})

    def test_invalid_signup(self):
        """ Register user that already exists."""

        data = {
            'email': 'mmitch@gmail.com',
            'username': 'mmitch',
            'password': '1234'
        }

        response = self.client.post(reverse('register'), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'status': 'user_exists'})

    def test_login(self):
        response = self.client.post(
            reverse('login'),
            self.user_data, format='json'
        )

        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        login_response = self.client.post(
            reverse('login'),
            self.user_data, format='json'
        )
        user_id = get_user_id(login_response.data['access'])

        post_data = {
            "title": 'Some post',
            "content": 'Some content',
            "author": user_id
        }

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}'
        )

        response = self.client.post(reverse('post-list'), post_data)

        post_from_db = Post.objects.all().first()

        self.assertEqual(response.status_code, 201)
        self.assertCountEqual(post_data['title'], post_from_db.title)

    def tearDown(self):
        User.objects.all().delete()


class LikeUnlikeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mmitch',
            email='mmitch@email.com',
            password='1234'
        )
        self.user_data = {
            'username': self.user.username,
            'password': '1234'
        }

        self.post_data = {
            "title": 'Some post',
            "content": 'Some content',
            "author": None
        }

        login_response = self.client.post(
            reverse('login'),
            self.user_data, format='json'
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}'
        )

        user_id = get_user_id(login_response.data['access'])

        self.post_data['author'] = user_id

        self.post = self.client.post(reverse('post-list'), self.post_data)

    def test_like_unlike(self):
        post_from_db = Post.objects.all().first()

        response = self.client.post(
            reverse('post-detail', args=[post_from_db.id]),
            data={'action': 'like'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_from_db.like.count(), 1)
        self.assertIn(self.user, post_from_db.like.all())

        response = self.client.post(
            reverse('post-detail', args=[post_from_db.id]),
            data={'action': 'unlike'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_from_db.like.count(), 0)
        self.assertNotIn(self.user, post_from_db.like.all())

    def test_anonymous_like(self):
        self.client.logout()

        post_from_db = Post.objects.all().first()

        response = self.client.post(
            reverse('post-detail', args=[post_from_db.id]),
            data={'action': 'like'}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(post_from_db.like.count(), 0)
        self.assertNotIn(self.user, post_from_db.like.all())

    def test_bad_request(self):
        post_from_db = Post.objects.all().first()

        response = self.client.post(
            reverse('post-detail', args=[post_from_db.id]),
            data={'action': 'bad_like'}
        )

        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
