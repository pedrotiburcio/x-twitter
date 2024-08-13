from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tweet(models.Model):
    """Um Tweet feito por um usuário."""
    text = models.CharField(max_length=280)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name ="tweet_like", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.text
        


