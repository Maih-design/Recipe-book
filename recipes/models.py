from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    categoty = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    ingrediants = models.TextField()
    directions = models.TextField()
    public = models.BooleanField(default=True)
    
class Rating(models.Model):
    rating_options = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rating_options)
    
class Comment(models.Model):
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.SET('unidentified user'))
    commentText = models.TextField()
    isReplay = models.BooleanField(default=False)
    parentCommentId = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.id)
    
class Favorate(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)