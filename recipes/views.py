from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import Recipe, Favorate, Rating, Comment
from .serializers import RecipesSerializer, RatingSerializer, CommentSerializer, FavorateSerializer
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import permission_classes, api_view

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

class MyRecipesView(viewsets.ViewSet):
    authentication_classes = [IsAuthenticated]
    def list(self, request):
        # item_name = request.query_params.get('title')
        # item_category = request.query_params.get('caregory')
        # item_contain = request.query_params.get('ingrediant')
        user = request.user
        items = Recipe.objects.filter(user=self.request.user)
        # if item_name:
        #     items = items.filter(name=item_name)
        # if item_category:
        #     items = items.filter(category=item_category)
        # if item_contain:
        #     items = items.filter(ingredients__contains=item_contain)
        serialized_items = RecipesSerializer(items, many=True)
        return Response(serialized_items.data)
    def create(self, request):
        serialized_item = RecipesSerializer(dtat=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data)
    def retrieve(self, request, id):
        item = get_object_or_404(Recipe, id=id)
        serialized_item = RecipesSerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)
    def update(self, request, id=id):
        item = get_object_or_404(Recipe, id=id)
        serialized_item = RecipesSerializer(item)
        if serialized_item.user == request.user:
            serialized_item = RatingSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"message":"you are not authorized"}, 403)
    def partial_update(self, request, id=id):
        item = get_object_or_404(Recipe, id=id)
        serialized_item = RecipesSerializer(item)
        if serialized_item.user == request.user:
            serialized_item = RatingSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({"message":"you are not authorized"}, 403) 
    def destroy(self, request, id=id):
        item = get_object_or_404(Recipe, id=id)
        serialized_item = RecipesSerializer(item)
        if serialized_item.user == request.user:
            serialized_item.delete()
            return Response({"message":"Recipe is deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"you are not authorized"}, 403) 

@api_view() 
@permission_classes([IsAdminUser])
def recipesview(request):
    item_name = request.query_params.get('title')
    item_category = request.query_params.get('caregory')
    item_contain = request.query_params.get('ingrediant')
    items = Recipe.objects.filter(public=True)
    if item_name:
        items = items.filter(name=item_name)
    if item_category:
        items = items.filter(category=item_category)
    if item_contain:
        items = items.filter(ingredients__contains=item_contain)
    serialized_items = RecipesSerializer(items, many=True)
    return Response(serialized_items.data)

@api_view('GET', 'POST', 'PATCH')
@permission_classes([IsAuthenticated])
def rating(request):
    recipe_id = request.query_params.get('recipe-id')
    if request.method == 'GET':
        recipe_rating = Rating.objects.filter(recipeId=recipe_id)
        if recipe_rating:
            serialiced_rating = RatingSerializer(recipe_rating)
            return Response(serialiced_rating.data)
        else:
            return Response({"message":"This recipe is not rated by any user yet"})
    if request.method == 'POST':
        
        recipe_rating = {
            'recipeId': recipe_id,
            'rating':,
            'num_of_rates': 
        }
        serialized_rating = RatingSerializer(data=)