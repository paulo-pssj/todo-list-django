from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    title = models.CharField(max_length=50, default='untitled')
    created_at = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        null=True,
        related_name="todolists", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.title
    
    def count(self):
        return self.todos.count()
    
    def count_finished(self):
        return self.todos.filter(is_finished=True).count()
    
    def count_open(self):
        return self.todos.filter(is_finished=False).count()
        
class Todo(models.Model):
    description = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User,
        null=True,
        related_name="todos",
        on_delete=models.CASCADE
    )
    todolist = models.ForeignKey(
        TodoList,
        related_name="todos",
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        self.description
        
    def close(self):
        self.is_finished = True
        self.save()
        
    def reopen(self):
        self.is_finished = False
        self.save()