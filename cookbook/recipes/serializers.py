from rest_framework import serializers

from .models import Ingredient, Product, Recipe


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "number_of_uses"]


class IngredientSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Ingredient
        fields = ["product", "weight"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ["id", "name", "ingredients"]


class AddProductToRecipeSerializer(serializers.Serializer):
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), required=True, source="recipe"
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=True, source="product"
    )
    weight = serializers.IntegerField(min_value=1)


class CookRecipeSerializer(serializers.Serializer):
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), required=True, source="recipe"
    )
