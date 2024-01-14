from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('myrecipes', views.MyRecipesView.as_view({
        'get': 'list', 
        'post': 'create'
    })),
    path('myrecipes/<int:pk>', views.MyRecipesView.as_view({
        'get': 'retrive', 
        'put': 'update', 
        'patch': 'partial-update', 
        'delete': 'destroy'
    })),
    path('recipes', views.recipesview),
    path('rating/<int:recipeId>', views.ratingview, name='rating'),
    path('favorates', views.FavorateView.as_view({'get': 'list'})),
    path('favorates/<int:recipeId>',views.FavorateView.as_view({'post': 'create'})),
]