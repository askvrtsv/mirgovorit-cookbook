from django.contrib import admin

from .models import Ingredient, Product, Recipe


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "number_of_uses"]
    list_display = ["name", "number_of_uses"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ["name"]
    inlines = [IngredientInline]
    list_display = ["name"]
