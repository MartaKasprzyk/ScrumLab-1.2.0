import random
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from jedzonko.models import Recipe, RecipePlan, Plan, DayName

class IndexView(View):

    def get(self, request):
        recipes = list(Recipe.objects.all())
        num_recipes = len(recipes)

        if num_recipes >= 3:
            recipes_mixed = random.sample(recipes, 3)
        else:
            recipes_mixed = recipes

        return render(request, "index.html", {"recipes_mixed": recipes_mixed})


class Dashboard(View):

    def get(self, request):
        number_of_recipes = Recipe.objects.all().count()
        number_of_plans = Plan.objects.all().count()
        latest_plan = Plan.objects.order_by('-created').first()
        recipe_plan = RecipePlan.objects.all().filter(plan=latest_plan)
        distinct_days = recipe_plan.distinct('day_name')
        return render(request, "dashboard.html", {'number_of_recipes': number_of_recipes,
                                                  'number_of_plans': number_of_plans, 'latest_plan': latest_plan,
                                                  'distinct_days': distinct_days, 'recipe_plan': recipe_plan})


class RecipesView(View):

    def get(self, request):
        paginator = Paginator(Recipe.objects.all().order_by('-votes', '-created').values(), 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "app-recipes.html", {'recipes': recipes})


class AddRecipe(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get('name').strip()
        ingredients = request.POST.get('ingredients').strip()
        description = request.POST.get('description').strip()
        preparation_time = request.POST.get('preparation_time')
        preparation_method = request.POST.get('preparation_method').strip()

        if name == "" or ingredients == "" or description == "" or preparation_time == "" or preparation_method == "":
            messages.info(request, "Wypełnij poprawnie wszystkie pola")
            return redirect("add_recipe")
        else:
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=preparation_time, preparation_method=preparation_method)
            return redirect("app_recipes")


class RecipeDetails(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        ingredients = recipe.ingredients
        ingredients = ingredients.split(',')
        return render(request, "app-recipe-details.html", {'recipe': recipe, 'ingredients': ingredients})

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if "like" in request.POST:
            recipe.votes += 1
            recipe.save()
        elif "dislike" in request.POST:
            recipe.votes -= 1
            recipe.save()
        return redirect('recipe_details', id=id)


class EditRecipe(View):

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        ingredients = recipe.ingredients
        ingredients = ingredients.split(',')
        return render(request, "app-edit-recipe.html", {"recipe": recipe, 'ingredients': ingredients})

    def post(self, request, id):
        Recipe.objects.get(id=id)
        name = request.POST.get('name').strip()
        ingredients = request.POST.get('ingredients').strip()
        description = request.POST.get('description').strip()
        preparation_time = request.POST.get('preparation_time')
        preparation_method = request.POST.get('preparation_method').strip()

        if name == "" or ingredients == "" or description == "" or preparation_time == "" or preparation_method == "":
            messages.info(request, "Wypełnij poprawnie wszystkie pola")
            return redirect("edit_recipe", id=id)
        else:
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=preparation_time, preparation_method=preparation_method)
            return redirect("app_recipes")


class ScheduleDetails(View):

    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        recipe_plan = RecipePlan.objects.all().filter(plan=plan)
        distinct_days = recipe_plan.distinct('day_name')

        return render(request, "app-details-schedules.html", {"plan": plan,
                                                              "recipe_plan": recipe_plan,
                                                              "distinct_days": distinct_days})


class AddSchedule(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name == "" or description == "":
            messages.info(request, "Wypełnij poprawnie wszystkie pola")
            return redirect("add_schedule")
        else:
            plan = Plan.objects.create(name=name, description=description)
            return redirect("schedule_details", plan.id)


class SchedulesList(View):

    def get(self, request):
        paginator = Paginator(Plan.objects.all().order_by('name').values(), 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "app-schedules.html", {'plans': plans})


class AddRecipeToSchedule(View):

    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all().order_by('order')
        return render(request, 'app-schedules-meal-recipe.html',
                      {'plans': plans, 'recipes': recipes, 'days': days})

    def post(self, request):
        plan_id = request.POST.get('choosePlan')
        meal_name = request.POST.get('name')
        meal_number = request.POST.get('number')
        recipe_id = request.POST.get('recipe')
        day_id = request.POST.get('day')

        RecipePlan.objects.create(meal_name=meal_name, order=meal_number, day_name_id=day_id,
                                  plan_id=plan_id, recipe_id=recipe_id)

        return redirect("schedule_details", plan_id)
