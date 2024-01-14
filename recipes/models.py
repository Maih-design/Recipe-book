from django.db import models
from django.contrib.auth.models import User 
from django.db.models import Avg

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    categoty = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='images/')
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
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
def create_or_update_rating(recipe_id):
    ratings = UserRatings.objects.filter(recipeId=recipe_id)
    average_rating = ratings.aaggregate(Avg('rating'))['rating__avg']
    rating_instance, created = Rating.objects.get_or_create(recipeId=recipe_id)
    rating_instance.rating = int(average_rating)
    rating_instance.num_of_rates = ratings.count()
    rating_instance.save()
    
class Rating(models.Model):
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    num_of_rates = models.IntegerField(default=1)
    
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
