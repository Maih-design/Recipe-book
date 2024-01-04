from rest_framework import serializers
from .models import Recipe, Rating, Comment, Favorate
from django.contrib.auth.models import User 

class RecipesSerializer(serializers.Serializer):
    user = serializers.HiddenField(default= serializers.CurrentUserDefault())
    class Meta:
        model = Recipe
        fields = "__all__"
    
class RatingSerializer(serializers.Serializer):
    rating = serializers.SerializerMethodField(method_name='calculate_rating')
    class Meta:
        model = Rating
        fields = "__all__"
    def calculate_rating(self, obj):
        current_rating = obj.rating
        num_of_rates = obj.num_of_rates
        new_rating = self.context['data'].get('rating', 0)
        rating = ((current_rating * num_of_rates) + new_rating)/(num_of_rates + 1)
        return rating

class CommentSerializer(serializers.Serializer):
    model = Comment
    fields = "__all__"
    
class FavorateSerializer(serializers.Serializer):
    model = Favorate
    fields = "__all__"