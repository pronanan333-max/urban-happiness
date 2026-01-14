from django.db import models

from account.models import CustomUser

class Article(models.Model):

    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(max_length=10000)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(CustomUser, max_length=10, on_delete=models.CASCADE, null=True)
    
    

    def __str__(self):
        return self.title