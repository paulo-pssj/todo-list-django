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
        self.assertTemplateUsed(response, "register.html")
        self.assertIsInstance(response.context['form'], RegisterForm)
        
    def test_get_login(self):
        """ Check if the login page exists and if its fields are correct """
        response = self.client.get(reverse("auth:login"))
        self.assertTemplateUsed(response, 'login.html')
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
        self.assertEqual(self.client.session["_auth_user_id"], 1)