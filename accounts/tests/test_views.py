from rest_framework.test import APIClient,APIRequestFactory,force_authenticate,APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.views import UserView

class TestUserRegisterView(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('accounts:register'),
                                    data={'email': 'mahdi@gmail.com', 'password': '12345678', 'c_password': '12345678'})
        self.assertEqual(response.status_code, 200)

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:register'),
                                    data={'email': 'mahdi', 'password': '12345678', 'c_password': '12345678'})
        self.assertEqual(response.status_code, 400)


class TestUserView(APITestCase):
    def setUp(self):
        user = get_user_model()
        u = user.objects.create_user(email='root@gmail.com', password='12345678')
        self.client = APIClient()
        self.client.force_authenticate(user=u)

    def test_user_GET(self):
        response = self.client.get('/auth/who/')
        self.assertEqual(response.status_code, 200)


class TestUserViewWithFactory(APITestCase):
    def setUp(self):
        user = get_user_model()
        self.u = user.objects.create_user(email='root@gmail.com', password='12345678')
        self.client = APIRequestFactory()

    def test_user_GET(self):
        request = self.client.get(reverse('accounts:user'))
        force_authenticate(request, user=self.u)
        response = UserView.as_view()(request).render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'root@gmail.com')

