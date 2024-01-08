from rest_framework import serializers
from .models import Recipe, Rating, Comment, Favorate
from django.contrib.auth.models import User 

class RecipesSerializer(serializers.Serializer):
    user = serializers.HiddenField(default= serializers.CurrentUserDefault())
    class Meta:
        model = Recipe
        fields = "__all__"
    
class RatingSerializer(serializers.Serializer):
    class Meta:
        model = Rating
        fields = "__all__"
    def calculate_rating(self, current_rating, new_rating, num_of_rates):
        rating = ((current_rating * num_of_rates) + new_rating)/(num_of_rates)
        return rating
    def pre_save(self, obj):
        obj.num_of_rates += 1
        obj.rating = self.calculate_rating(obj.rating, request.data['rating'], obj.num_of_rates)                          , 
        return obj

class CommentSerializer(serializers.Serializer):
    model = Comment
    fields = "__all__"
    
class FavorateSerializer(serializers.Serializer):
    model = Favorate
    fields = "__all__"
