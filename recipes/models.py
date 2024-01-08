from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    categoty = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingrediants = models.TextField(db_index=True)
    directions = models.TextField()
    public = models.BooleanField(default=True)

class UserRatings(models.Model):
    rating_options = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rating_options)
    class Meta:
        unique_together = (('userId', 'recipeId'),)
    
class Rating(models.Model):
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    num_of_rates = models.IntegerField()
    
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
