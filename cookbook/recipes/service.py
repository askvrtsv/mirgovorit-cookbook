from django.db.models import F

from . import serializers
from .models import Ingredient, Product, Recipe


def get_recipes(product_id: int, max_weight: int) -> list[Recipe]:
    """
    Возвращает рецепты, для которых не нужен указанный товар,
    либо вес этого товара меньше указанного.
    """
    return (
        Recipe.objects.prefetch_related("ingredients__product")
        .exclude(
            ingredients__in=Ingredient.objects.filter(
                product_id=product_id, weight__gte=max_weight
            )
        )
        .all()
    )


def add_ingredient(recipe: Recipe, product: Product, weight: int) -> None:
    """
    Добавляет новый ингредиент в рецепт или обновляет его вес,
    если он уже имеется.
    """
    recipe.ingredients.update_or_create(
        recipe=recipe,
        product=product,
        defaults={"weight": weight},
    )


def update_ingredient_uses(recipe: Recipe) -> None:
    """
    Увеличивает на единицу число используемых продуктов в указанном рецепте.
    """
    using_product_ids = recipe.ingredients.values_list("product__id", flat=True)
    Product.objects.filter(id__in=(using_product_ids)).update(
        number_of_uses=F("number_of_uses") + 1
    )


def get_recipe_serializer(recipe_id: int) -> serializers.RecipeSerializer:
    return serializers.RecipeSerializer(
        Recipe.objects.prefetch_related("ingredients__product").get(pk=recipe_id)
    )
