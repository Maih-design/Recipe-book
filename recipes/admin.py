from django.contrib import admin
from .models import Recipe, Rating, Comment, Favorate

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Favorate)