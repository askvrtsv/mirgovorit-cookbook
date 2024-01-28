from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers, service
from .constants import RECIPES_MAX_PRODUCT_WEIGHT
from .models import Product


def show_recipes_without_product(request: HttpRequest) -> HttpResponse:
    """
    Функция возвращает HTML страницу, на которой размещена таблица. В таблице
    отображены id и названия всех рецептов, в которых указанный продукт
    отсутствует, или имеется в количестве меньше 10 грамм.
    """
    try:
        product_id = int(request.GET.get("product_id") or -1)
        product = Product.objects.get(pk=product_id)
    except (ValueError, Product.DoesNotExist):
        product_id = -1
        product = None

    return render(
        request,
        "show_recipes_without_product.html",
        context={
            "product": product,
            "recipes": service.get_recipes(
                product_id, max_weight=RECIPES_MAX_PRODUCT_WEIGHT
            ),
            "max_weight": RECIPES_MAX_PRODUCT_WEIGHT,
        },
    )


@api_view(["GET"])
def add_product_to_recipe(request: Request) -> Response:
    """
    Функция добавляет к указанному рецепту указанный продукт с указанным весом.
    Если в рецепте уже есть такой продукт, то функция должна поменять его вес
    в этом рецепте на указанный.
    """
    serializer_in = serializers.AddProductToRecipeSerializer(data=request.GET)
    if serializer_in.is_valid(raise_exception=True):
        service.add_ingredient(
            serializer_in.validated_data["recipe"],
            serializer_in.validated_data["product"],
            serializer_in.validated_data["weight"],
        )
    serializer_out = service.get_recipe_serializer(
        serializer_in.validated_data["recipe"].id
    )
    return Response(serializer_out.data)


@api_view(["GET"])
def cook_recipe(request: Request) -> Response:
    """
    Функция увеличивает на единицу количество приготовленных блюд для каждого
    продукта, входящего в указанный рецепт.
    """
    serializer_in = serializers.CookRecipeSerializer(data=request.GET)
    if serializer_in.is_valid(raise_exception=True):
        service.update_ingredient_uses(serializer_in.validated_data["recipe"])
    serializer_out = service.get_recipe_serializer(
        serializer_in.validated_data["recipe"].id
    )
    return Response(serializer_out.data)
