from django import forms 
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), label="password")
    
    def clean(self):
        
        if self.errors:
            return self.cleaned_data
        
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username).first()
        
        if not user or not user.check_password(password):
            raise forms.ValidationError("Incorrect username and/or password.")
        
        return self.cleaned_data
    
    
class RegisterForm(forms.Form):
    
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        
        if password and password != password_confirmation:
            raise forms.ValidationError("password don't match.")
    
        return self.cleaned_data