from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    userName = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.name + " " + self.lastName
        
class Tweet(models.Model):
    """Um Tweet feito por um usuário."""
    text = models.CharField(max_length=280)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.text
        


