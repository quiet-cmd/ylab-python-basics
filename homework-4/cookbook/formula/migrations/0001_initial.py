# Generated by Django 3.2.8 on 2021-10-29 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название блюда')),
                ('author', models.CharField(max_length=255, verbose_name='Автор')),
                ('photo', models.ImageField(upload_to='dish', verbose_name='Фотография блюда')),
                ('cooking_time', models.IntegerField(verbose_name=' Время готовки')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Обложка рецепта',
                'verbose_name_plural': 'Обложки рецептов',
                'ordering': ['time_create', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('instruction', models.TextField(verbose_name='Способ пригтовления')),
                ('proteins', models.FloatField(verbose_name='Количество белка')),
                ('fats', models.FloatField(verbose_name='Количество жиров')),
                ('carbohydrates', models.FloatField(verbose_name='Количество углеводов')),
                ('calories', models.FloatField(verbose_name='Количество калорий')),
                ('cover', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='formula.cover')),
            ],
            options={
                'verbose_name': 'Рецепт и его пищевая ценность',
            },
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredients_name', models.CharField(max_length=64, verbose_name='Название продукта')),
                ('amount', models.TextField(max_length=64, verbose_name='Количество продукта')),
                ('recipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='formula.cover')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
