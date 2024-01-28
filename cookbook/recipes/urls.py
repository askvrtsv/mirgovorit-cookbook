from django.urls import path

from . import views

urlpatterns = [
    path("show_recipes_without_product/", views.show_recipes_without_product),
    path("api/add_product_to_recipe/", views.add_product_to_recipe),
    path("api/cook_recipe/", views.cook_recipe),
]
