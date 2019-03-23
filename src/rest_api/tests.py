from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_api.urls import TokenObtainPairView
from django.urls import reverse


class UserTest(APITestCase):
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

        response = self.client.post(
            '/api/v1/signup/',
            data,
            content_type='application/json'
        )

        user = User.objects.get(pk=2)

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

        response = self.client.post(
            '/api/v1/signup/',
            data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'status': 'user_exists'})

    def test_login(self):
        response = self.client.post(
            '/api/v1/login/',
            self.user_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.client.defaults['Authorization'] = response.data['access']

    def test_create_post(self):
        login_response = self.client.post(
            reverse('login'),
            self.user_data,
            format='json'
        )

        import ipdb
        ipdb.set_trace()

        self.client.credentials(HTTP_AUTHORIZATION=f'Baerer {login_response.data["access"]}')
        response = self.client.get(reverse('post-list'))

        ipdb.set_trace()




    def tearDown(self):
        User.objects.all().delete()