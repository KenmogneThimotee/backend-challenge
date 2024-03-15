from django.forms import ValidationError
from django.test import TestCase
from user_management.models import User, UserManager

class UserTestCase(TestCase):
    
    # Creating a new user with valid email, password, first name, and last name should successfully create a new user object.
    def test_create_user_with_valid_details(self):
        email = "test@example.com"
        password = "password123"
        first_name = "John"
        last_name = "Doe"
    
        user = User.objects.create_user(email, password, first_name, last_name)
        
        user.full_clean()
    
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))
        
    # Creating a new user with an invalid email should raise a validation error.
    def test_create_user_with_invalid_email(self):
        email = "invalid_email"
        password = "password123"
        first_name = "John"
        last_name = "Doe"

        user = User.objects.create(email=email, password=password, first_name=first_name, last_name=last_name)
        
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    def test_update_user_email_existing_email(self):
    
        email = 'user@example.com'
        password = 'Password123'
        first_name = 'John'
        last_name = 'Doe'
        
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    


      

