# app/tests/test_setup.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.models import User
from tasks.models import Label

class TestLabelAPI(TestCase):

    def setUp(self):
        self.base_url = "/labels/"
        self.client = APIClient()
        fake_email = "user@exanple.com"
        self.user = User.objects.create(
            email=fake_email
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    
    def test_create_label(self):
        
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_label_with_tasks(self):
        
        url = '/tasks/'
        task_response1 = self.client.post(url, {
            'title': 'Test Title 1',
            'description': "Test description",
            'priority': 1,
        })
        
        task_response2 = self.client.post(url, {
            'title': 'Test Title 2',
            'description': "Test description",
            'priority': 1,
        })
        
        label_response = self.client.post(self.base_url, {
            'name': 'Test label',
            'tasks': [task_response1.data['id'], task_response2.data['id']]
        })
        
        self.assertEqual(label_response.status_code, status.HTTP_201_CREATED)
        
    def test_retrieve_label(self):
        
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })
        
        url = f"/labels/{response.data['id']}/"
        response = self.client.get(url)
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test label')
    
        

    def test_update_label(self):
        
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })
    
        response = self.client.patch(f"{self.base_url}{response.data['id']}/", {
            'name': 'Updated label',
        })
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated label')

    def test_update_label_with_tasks(self):
        
        url = '/tasks/'
        task_response1 = self.client.post(url, {
            'title': 'Test Title 1',
            'description': "Test description",
            'priority': 1,
        })
        
        task_response2 = self.client.post(url, {
            'title': 'Test Title 2',
            'description': "Test description",
            'priority': 1,
        })
        
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })
    
        response = self.client.patch(f"{self.base_url}{response.data['id']}/", {
            'name': 'Updated label',
            'tasks': [task_response1.data['id'], task_response2.data['id']]
            
        })
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated label')
        self.assertListEqual(response.data['tasks'], [task_response1.data['id'], task_response2.data['id']])


    def test_create_label_without_name(self):
    
        response = self.client.post(self.base_url, {})
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], 'This field is required.')

    def test_update_nonexistent_label(self):
        label_id = 9999
    
        response = self.client.put(f"{self.base_url}{label_id}/", {
            'name': 'Updated label',
        })
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_label_with_empty_name(self):
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })
    
        response = self.client.put(f"{self.base_url}{response.data['id']}/", {
            'name': '',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')

    def test_create_label_without_credentials(self):

        client = APIClient() # Remove user credentials

        response = client.post(self.base_url, {
            'name': 'Test label',
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_duplicate_label_name(self):
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })

        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_label(self):
        response = self.client.post(self.base_url, {
            'name': 'Test label',
        })

        response = self.client.delete(f"{self.base_url}{response.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_label(self):

        response = self.client.delete(f"{self.base_url}{2}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_retrieve_label_related_owner(self):
        
        user = User.objects.create(email="user@example.com", first_name="Thimotee",
                                   last_name="Legrand", password="Xandercage03")

        user.save()
        
        label1 = Label.objects.create(
            name='Test Label 1',
            created_by=user
        )
        
        label2 = Label.objects.create(
            name='Test Label 2',
            created_by=user
        )
        
        label1.save()
        label2.save()
        
        response1 = self.client.post(self.base_url,{
            'name': 'Owner  Test Label 1',
        })
        
        response2 = self.client.post(self.base_url,{
            'name': 'Owner  Test label 2',
        })
        
        response = self.client.get(self.base_url)
        
        self.assertDictEqual(response.data[0], response1.data)
        self.assertDictEqual(response.data[1], response2.data)
        self.assertTrue(response.status_code == status.HTTP_200_OK)