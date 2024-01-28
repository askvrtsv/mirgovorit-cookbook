from core.models import DefaultModel
from django.db import models


class Product(DefaultModel):
    name = models.CharField("название", max_length=255, unique=True)
    number_of_uses = models.IntegerField("кол-во использований", default=0)
    recipes = models.ManyToManyField(
        "Recipe", through="Ingredient", verbose_name="рецепты"
    )

    class Meta:
        db_table = "products"
        ordering = ["name"]
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Recipe(DefaultModel):
    name = models.CharField("название", max_length=255)

    class Meta:
        db_table = "recipes"
        ordering = ["name"]
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"


class Ingredient(DefaultModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="рецепт",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="продукт"
    )
    # Вес в граммах
    weight = models.PositiveSmallIntegerField("вес, гр")

    class Meta:
        db_table = "ingredients"
        ordering = ["-weight", "product__name"]
        unique_together = ["recipe", "product"]
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
