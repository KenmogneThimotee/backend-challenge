
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from user_management.models import User, UserManager


class AUTHTestCase(TestCase):
    
    def test_signup_success(self):
        
        client = APIClient()
        
        url = reverse("auth_register")
        
        response = client.post(url, {'email':'user@example.com', 'password':'Xandercage03',  'password2':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_signup_fail_missing_fields(self):
        
        client = APIClient()
        
        url = reverse("auth_register")
        
        response = client.post(url, {'email':'user@example.com', 'password':'Xandercage03', 'password2':'Xandercage03'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_signup_fail_existing_email(self):
        client = APIClient()
        url = reverse("auth_register")
        client.post(url, {'email':'user@example.com', 'password':'Xandercage03',  'password2':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        response = client.post(url, {'email':'user@example.com', 'password':'Xandercage03',  'password2':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_missing_password(self):
        client = APIClient()
        url = reverse("auth_register")
        response = client.post(url, {'email':'user@example.com', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_signup_invalid_email_format(self):
        client = APIClient()
        url = reverse("auth_register")
        response = client.post(url, {'email':'invalid_email', 'password':'Xandercage03', 'password2':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success_token_returned(self):
        url = reverse('token_obtain_pair')
        u = User.objects.create_user(**{'email':'user@example.com', 'password':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        u.save()

        response = self.client.post(url, {'email':'user@example.com', 'password':'Xandercage03'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_login_fail_invalid_password(self):
        url = reverse('token_obtain_pair')
        u = User.objects.create_user(**{'email':'user@example.com', 'password':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        u.save()

        response = self.client.post(url, {'email':'user@example.com', 'password':'InvalidPassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_user_fail_empty_email(self):
        client = APIClient()
        url = reverse("auth_register")
        response = client.post(url, {'email':'', 'password':'Xandercage03', 'password2':'Xandercage03', 'first_name': 'Thimotee', 'last_name': 'legrand'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
