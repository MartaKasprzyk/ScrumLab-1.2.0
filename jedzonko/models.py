from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)
    preparation_method = models.TextField(blank=True)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan") 


class DayName(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
