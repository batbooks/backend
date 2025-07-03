from django.test import TestCase
from accounts.serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model


class TestUserRegisterSerializer(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        user_model.objects.create_user(email='ali@gmail.com', password='123')

    def test_valid_data(self):
        ser_data = UserRegisterSerializer(
            data={'email': 'mahdi@gmail.com', 'password': 'mahdi123', 'c_password': 'mahdi123'})
        self.assertTrue(ser_data.is_valid())

    def test_empty_data(self):
        ser_data = UserRegisterSerializer(data={})
        self.assertFalse(ser_data.is_valid())
        self.assertEqual(len(ser_data.errors), 3)

    def test_duplicate_email(self):
        ser_data = UserRegisterSerializer(
            data={'email': 'ali@gmail.com', 'password': '12345678', 'c_password': '12345678'})
        self.assertFalse(ser_data.is_valid())
        self.assertIn('email', ser_data.errors)
        self.assertIn('user with this email already exists', str(ser_data.errors['email']).lower())

    def test_invalid_password(self):
        ser_data = UserRegisterSerializer(
            data={'email': 'ali1@gmail.com', 'password': '123', 'c_password': '123'}
        )
        self.assertFalse(ser_data.is_valid())
        self.assertEqual(len(ser_data.errors), 1)
        self.assertTrue(ser_data.errors['password'])

    def test_unmatched_password(self):
        ser_data = UserRegisterSerializer(
            data={'email': 'ali1@gmail.com', 'password': '12345678', 'c_password': '12345679'}
        )
        self.assertFalse(ser_data.is_valid())
        self.assertEqual(len(ser_data.errors), 1)
        self.assertIn('error', ser_data.errors)
        self.assertEqual(
            ser_data.errors['error'][0],
            "گذرواژه‌ها یکسان نیستند."
        )

