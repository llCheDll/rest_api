from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client
from rest_api.views import RegisterView
from rest_api.urls import TokenObtainPairView

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.factory = RequestFactory()
        # self.user = User.objects.create_user(
        #     username='mmitch', email='mmitch@gmail.com', password='1234')
        # import ipdb
        # ipdb.set_trace()

    def test_signup(self):
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'user_create'})

    def test_login(self):
        import ipdb
        ipdb.set_trace()
        # request = self.client.post(
        #     '/api/v1/login/',
        #     data,
        #     content_type='application/json'
        # )

        # request.user = AnonymousUser()
        # response = TokenObtainPairView.as_view()(request)

        # token_names = ['refresh', 'access']

        # self.assertEqual(response.status_code, 200)
        # self.assertEqual([name for name in response.data.keys()], token_names)

        # self.user.token = response.data['access']


