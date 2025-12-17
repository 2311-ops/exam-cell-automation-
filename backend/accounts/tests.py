from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginTests(APITestCase):
    def setUp(self):
        # create a test user
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=self.password,
            role='student'
        )

    def test_login_success(self):
        url = reverse('login')
        resp = self.client.post(url, {'username': 'testuser', 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_login_missing_username(self):
        url = reverse('login')
        resp = self.client.post(url, {'password': self.password}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('non_field_errors', resp.data)  # serializer will raise ValidationError
