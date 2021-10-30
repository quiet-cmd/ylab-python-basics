from django.contrib import admin
from .models import *


class IngredientsInline(admin.StackedInline):
     model = Ingredients
     extra = 1


class RecipeInline(admin.StackedInline):
    model = Recipe


class CoverAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time_create', 'time_update')
    inlines = [IngredientsInline, RecipeInline]
    search_fields = ('title', 'author', 'ingredients__ingredients_name')


admin.site.register(Cover, CoverAdmin)
