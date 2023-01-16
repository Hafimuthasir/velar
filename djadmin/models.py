from django.db import models
from djapp.models import Posts,User

# Create your models here.
class admins(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class PostReports(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    