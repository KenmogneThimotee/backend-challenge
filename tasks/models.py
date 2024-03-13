from django.db import models
from user_management.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['priority']
        

class Label(models.Model):
    name = models.CharField(max_length=50)
    tasks = models.ManyToManyField(Task)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']