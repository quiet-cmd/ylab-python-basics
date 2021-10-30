from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q

from .models import *


class Formulas(ListView):
    """Главная страница со всеми рецептами"""
    model = Cover
    template_name = 'formula/index.html'
    context_object_name = 'covers'


class SearchResults(ListView):
    """Поиск по автору, названию и продукту"""
    model = Cover
    template_name = 'formula/index.html'
    context_object_name = 'covers'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Cover.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(ingredients__ingredients_name=query)).order_by('id').distinct('id')
        return object_list


def formula(request, dish_id):
    """страница конкретного рецепта"""
    context = {
        'recipe': get_object_or_404(Recipe, cover=dish_id),
        'ingredients': Ingredients.objects.filter(recipe=dish_id),
        'covers': Cover.objects.get(id=dish_id)
    }
    return render(request, 'formula/formula.html', context=context)
