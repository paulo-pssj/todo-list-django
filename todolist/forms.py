from django import forms

class TodoForm(forms.Form):
    description = forms.CharField(max_length=200)
    
class TodoListForm(forms.Form):
    title = forms.CharField(max_length=50)