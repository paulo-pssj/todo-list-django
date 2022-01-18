from django.test import TestCase
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.forms import LoginForm, RegisterForm

class AccountsTest(TestCase):
    def setUp(self):
        self.register_data= {
            "email": "new@user.com",
            "username": "new_user",
            "password": "test",
            "password_confirmation": "test",
        }
        User.objects.create_user("test", "test@exemple.com", "test")
        
    def tearDown(self):
        User.objects.get(username="test").delete()
        
    def test_get_register(self):
        """ Check if the register page exists and if its fields are correct """
        response = self.client.get(reverse("auth:register"))
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context['form'], RegisterForm)
        
    def test_get_login(self):
        """ Check if the login page exists and if its fields are correct """
        response = self.client.get(reverse("auth:login"))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)
        
    def test_register(self):
        """ Check if new user is registered """
        response = self.client.post(reverse("auth:register"), data=self.register_data)
        self.assertRedirects(response, "/auth/login/")
        self.assertIsNotNone(User.objects.get(username="new_user"))
        
    def test_login(self):
        """ Checks if the process of login its OK """
        self.assertFalse("_auth_user_id" in self.client.session)
        login_data = {"username": "test", "password": "test"}
        response = self.client.post(reverse("auth:login"), data=login_data)
        self.assertRedirects(response, "/")
        self.assertEqual(self.client.session["_auth_user_id"], '1')
        
    def test_login_with_not_exist_user(self):
        """ Checks if login accept non existing user """
        login_data = {"username": "notuser", "password": "notpassword"}
        response = self.client.post(reverse("auth:login"), data=login_data)
        error_message = "Incorrect username and/or password."
        self.assertContains(response, error_message, status_code=200)
        
    def test_login_with_incorrect_password(self):
        """ Checks if login accept incorrect password"""
        login_data = {"username": "test", "password": "notpassword"}
        response = self.client.post(reverse("auth:login"), data=login_data)
        error_message = "Incorrect username and/or password."
        self.assertContains(response, error_message, status_code=200)
        
    def test_logout(self):
        """Checks if logout redirect for index"""
        response = self.client.get(reverse("auth:logout"))
        self.assertRedirects(response, "/")
        self.assertFalse("_auth_user_id" in self.client.session)