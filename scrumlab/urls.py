"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('/', views.IndexView.as_view(), name='index'),
    path('recipe/<int:id>/', views.RecipeDetails.as_view(), name='recipe_details'),
    path('recipe/add/', views.AddRecipe.as_view(), name='add_recipe'),
    path('recipe/modify/<int:id>/', views.EditRecipe.as_view(), name='edit_recipe'),
    path('plan/<int:id>/', views.ScheduleDetails.as_view(), name='schedule_details'),
    path('plan/add/', views.AddSchedule.as_view(), name='add_schedule'),
    path('plan/list/', views.SchedulesList.as_view(), name='schedules_list'),
    path('main/', views.Dashboard.as_view(), name='dashboard'),
    path('recipe/list/', views.RecipesView.as_view(), name='app_recipes'),
    path('plan/add-recipe/', views.AddRecipeToSchedule.as_view(), name='add_recipe_to_plan'),
]
