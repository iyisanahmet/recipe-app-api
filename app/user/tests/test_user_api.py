from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the user API(public)"""

    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        """Test creating user with valid is successfull"""
        payload = {
            'email':'test@test.com',
            'password':'passsword123',
            'name':'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data) 
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {
            "email":"test@test.com",
            'password':'test123'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 chars"""
        payload={
            'email':'test@test.com',
            'password':'pw'
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token created for the user"""
        payload = {"email":'teat@test.com','password':'testpassword'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com',password='testpasss')
        payload = {'email':'test@test.com','password':'wrong'}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if the user does not exist"""
        payload= {'email':'test@test.com','password':'password1'}
        res = self.client.post(TOKEN_URL,payload)
        
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are missing"""
        res = self.client.post(TOKEN_URL,{'email':'','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


         
 