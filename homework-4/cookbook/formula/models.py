from django.db import models


class Cover(models.Model):
    """Внешний вид рецепта на главной странице"""
    title = models.CharField(max_length=255, verbose_name='Название блюда')
    author = models.CharField(max_length=255, verbose_name='Автор')
    photo = models.ImageField(upload_to='dish', verbose_name='Фотография блюда')
    cooking_time = models.IntegerField(verbose_name=' Время готовки')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Обложка рецепта'
        verbose_name_plural = 'Обложки рецептов'
        ordering = ['-time_create', 'title']


# возможно стоит разделить таблицу на пищевая ценность и рецепт, рецепт сделать Inline
class Recipe(models.Model):
    """Инструкция + пищевая ценность"""
    instruction = models.TextField(verbose_name='Способ пригтовления')
    proteins = models.FloatField(verbose_name='Количество белка')
    fats = models.FloatField(verbose_name='Количество жиров')
    carbohydrates = models.FloatField(verbose_name='Количество углеводов')
    calories = models.FloatField(verbose_name='Количество калорий')
    cover = models.OneToOneField('Cover', on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = 'Рецепт и его пищевая ценность'


class Ingredients(models.Model):
    """Поле с ингредиентами и их количеством"""
    recipe = models.ForeignKey('Cover', on_delete=models.CASCADE, null=True, related_name="ingredients")
    ingredients_name = models.CharField(max_length=64, verbose_name='Название продукта')
    amount = models.TextField(max_length=64, verbose_name='Количество продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
