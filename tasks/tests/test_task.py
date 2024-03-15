# app/tests/test_setup.py

import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.models import User
from tasks.models import Task

class TestTaskAPI(TestCase):

    def setUp(self):
        self.base_url = "/tasks/"
        self.client = APIClient()
        fake_email = "user@exanple.com"
        self.user = User.objects.create(
            email=fake_email
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    
    def test_create_task(self):
        
        url = '/tasks/'
        response = self.client.post(url, {
            'title': 'Test Title',
            'description': "Test description",
            'priority': 1,
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_task(self):
        
        response = self.client.post(self.base_url,{
            'title': 'Test Title',
            'description': "Test description",
            'priority': 1,
        })
        
        url = f"/tasks/{response.data['id']}/"
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Title')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertEqual(response.data['priority'], 1)
    
    def test_create_task_without_credentials(self):

        client = APIClient() # Remove user credentials

        response = client.post(self.base_url,{
            'title': 'Test Title',
            'description': "Test description",
            'priority': 1,
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_task(self):
        
        response = self.client.post(self.base_url,{
            'title': 'Test Title',
            'description': "Test description",
            'priority': 1,
        })
        
        url = f"/tasks/{response.data['id']}/"
        response = self.client.put(url, {
            'title': 'Updated Title',
            'description': 'Updated description',
            'priority': 2
        })
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['description'], 'Updated description')
        self.assertEqual(response.data['priority'], 2)

    def test_create_task_without_title(self):
    
        response = self.client.post(self.base_url, {
            'description': "Test description",
            'priority': 1,
        })
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_task(self):
    
        response = self.client.get(self.base_url + "999/")
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_without_description(self):

        response = self.client.post(self.base_url, {
            'title': 'Test Title',
            'priority': 1,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_empty_title(self):

        response = self.client.post(self.base_url, {
            'title': '',
            'description': "Test description",
            'priority': 1,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_task_with_invalid_priority(self):
        response = self.client.post(self.base_url, {
            'title': 'Test Title',
            'description': "Test description",
            'priority': -3,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_task_success(self):
        
        response = self.client.post(self.base_url,{
            'title': 'Test Title',
            'description': "Test description",
            'priority': 1,
        })
        
        url = f"{self.base_url}{response.data['id']}/"
        response = self.client.delete(url)
    
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_task(self):
        
        response = self.client.delete(f"{self.base_url}2/")
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_retrieve_task_related_owner(self):
        
        user = User.objects.create(email="user@example.com", first_name="Thimotee",
                                   last_name="Legrand", password="Xandercage03")

        user.save()
        
        task1 = Task.objects.create(
            title='Test Title 1',
            description='Test description',
            priority=1,
            created_by=user
        )
        
        task2 = Task.objects.create(
            title='Test Title 2',
            description='Test description',
            priority=1,
            created_by=user
        )
        
        task1.save()
        task2.save()
        
        response1 = self.client.post(self.base_url,{
            'title': 'Owner  Test Task 1',
            'description': "Owner Test description 1",
            'priority': 5,
        })
        
        response2 = self.client.post(self.base_url,{
            'title': 'Owner  Test Task 2',
            'description': "Owner Test description 2",
            'priority': 5,
        })
        
        response = self.client.get(self.base_url)
        
        self.assertDictEqual(response.data[0], response1.data)
        self.assertDictEqual(response.data[1], response2.data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)