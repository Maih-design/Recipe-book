from rest_framework import serializers
from .models import Recipe, Rating, Comment, Favorate

class RecipesSerializer(serializers.Serializer):
    model = Recipe
    fields = "__all__"
    
class RatingSerializer(serializers.Serializer):
    model = Rating
    fields = "__all__"

class CommentSerializer(serializers.Serializer):
    model = Comment
    fields = "__all__"
    
class FavorateSerializer(serializers.Serializer):
    model = Favorate
    fields = "__all__"