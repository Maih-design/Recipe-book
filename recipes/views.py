from django.shortcuts import render
from rest_framework import generics, viewsets, status
from .models import Recipe, Favorate, Rating, Comment, UserRatings, create_or_update_rating
from .serializers import RecipesSerializer, UserRatingSerializer, CommentSerializer, FavorateSerializer, RatingSerializer
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
            serialized_item = RecipesSerializer(item, data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"message":"you are not authorized"}, 403)
    def partial_update(self, request, id=id):
        item = get_object_or_404(Recipe, id=id)
        serialized_item = RecipesSerializer(item)
        if serialized_item.user == request.user:
            serialized_item = RecipesSerializer(item, data=request.data)
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

# @api_view('GET', 'PATCH')
# @permission_classes([IsAuthenticated])
# def rating(request, recipe_id):
#     try:
#         rating = Rating.objects.get(recipe_id=recipe_id)
#     except rating.DoesNotExist:
#         rating = None
#     if request.method == 'GET':
#         if rating:
#             serialized_rating = RatingSerializer(rating)
#             return Response(serialized_rating.data)
#         else:
#             return Response({"message":"This recipe is not rated by any user yet"})
#     if request.method == 'PATCH':
#         if rating:
#             serialized_rating = RatingSerializer(rating, data=request.data, partial=True)
#             if serialized_rating.is_valid():
#                 serialized_rating.save()
#                 return Response(serialized_rating.data)
#             else:
#                 return Response(serialized_rating.errors, status = status.HTTP_400_BAD_REQUEST)
#         else:
#             serialized_rating = RatingSerializer(data=request.data)
#             if serialized_rating.is_valid():
#                 serialized_rating.save()
#                 return Response(serialized_rating.data)
#             else:
#                 return Response(serialized_rating.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ratingview(request, recipeId):
    user_id = request.user.id
    rating = request.query_params.get('rating')
    if request.method == 'POST':
        if not rating:
            item = UserRatings.objects.get(userId=user_id, recipeId=recipeId)
            if item:
                serializer = UserRatingSerializer(item)
                return Response(serializer.data)
            else:
                return Response({"message":"You didnt rate this recipe yet"})
        else:
            item = UserRatings.objects.get(userId=user_id, recipeId=recipeId)
            if item:
                serializer = UserRatingSerializer(item, rating=rating)
                if serializer.is_valid():
                    serializer.save()
                    create_or_update_rating(recipeId)
                    recipe_rating = Rating.objects.get(recipeId=recipeId)
                    recipe_rating_serializer = RatingSerializer(recipe_rating)
                    return Response(recipe_rating_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
                else:
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            else:
                serializer= UserRatingSerializer(data={'rating': rating, 'recipeId': recipeId, 'userId': user_id})
                if serializer.is_valid():
                    serializer.save()
                    create_or_update_rating(recipeId)
                    recipe_rating = Rating.objects.get(recipeId=recipeId)
                    recipe_rating_serializer = RatingSerializer(recipe_rating)
                    return Response(recipe_rating_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
                else:
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
        # serializer = UserRatingsSerializser(data=request.data)
        # if serializer.is_valid:
        #     serializer.save()
        #     try:
        #         rating = Rating.objects.get(recipeId=serializer.data['recipeId'])
        #     except rating.DoesNotExist:
        #         rating = None
        #     if rating:
        #         serialized_rating = RatingSerializer(rating)
        #         if serialized_rating.is_valid():
        #             serialized_rating.save()
        #             return Response(serialized_rating.data)
        #         else:
        #             return Response(serialized_rating.errors, status = status.HTTP_400_BAD_REQUEST)
        #     else:
        #         data = {
        #             'recipeId': RatingSerializer,
        #             'num_of_rates': 0
        #         }
        #         serialized_rating = RatingSerializer(data=data)
        #         if serialized_rating.is_valid:
        #             serialized_rating.save()
        #             return Response(serialized_rating.data)
        #         else:
        #             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def fav(request):
    if request.method == 'GET':
        favs = Favorate.objects.filter(userId=request.user.id, many=True)
        if favs:
            serializer = FavorateSerializer(favs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Your favorates list is empty."})
        
class FavorateView(viewsets.ViewSet):
    authentication_classes= [IsAuthenticated]
    def list(self,request):
        favs = Favorate.objects.filter(userId=request.user.id, many=True)
        if favs:
            serializer = FavorateSerializer(favs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Your favorates list is empty."})
    def create(self, request, recipeId):
        serialiver = FavorateSerializer(data={'userId': request.user.id, 'recipeId': recipeId})
        if serialiver.is_valid():
            serialiver.save()
            return Response(serialiver.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialiver.errors, status=status.HTTP_400_BAD_REQUEST)