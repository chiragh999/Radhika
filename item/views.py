from collections import defaultdict
from rest_framework.response import Response
from rest_framework import status, generics
from ListOfIngridients.models import IngridientsCategory
from ListOfIngridients.serializers import IngridientsCategorySerializer
from Radhika.Utils.permissions import *
from eventbooking.models import EventBooking
from .models import Item
from .serializers import *


# --------------------    ItemViewSet    --------------------


class ItemViewSet(generics.GenericAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request):
        if Item.objects.filter(name=request.data.get("name")).exists():
            return Response(
                {
                    "status": False,
                    "message": "Item already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Item created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": False,
                "message": "Something went wrong",
                "data": {},
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        # Get all item IDs that are already used in RecipeIngredient
        used_item_ids = set(RecipeIngredient.objects.values_list("item__pk", flat=True))

        # Exclude those items from the queryset
        available_items = Item.objects.exclude(id__in=used_item_ids)

        # Serialize the queryset
        serializer = ItemSerializer(available_items, many=True)

        return Response(
            {
                "status": True,
                "message": "Item list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ItemGetViewSet(generics.GenericAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def put(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Item updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "status": False,
                    "message": "Something went wrong",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(
                {
                    "status": True,
                    "message": "Item retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return Response(
                {
                    "status": True,
                    "message": "Item deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    RecipeIngredientViewSet    --------------------


class RecipeIngredientViewSet(generics.GenericAPIView):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request):
        serializer = RecipeIngredientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Recipe Ingredient created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": False,
                "message": "Something went wrong",
                "data": {},
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        recipe_ingredient = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredient, many=True)
        for data in serializer.data:
            item = Item.objects.filter(pk=data.get("item")).values("name").first()
            data["item"] = item
        return Response(
            {
                "status": True,
                "message": "Recipe Ingredient List",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class EditRecipeIngredientViewSet(generics.GenericAPIView):
    serializer_class = EditRecipeIngredientSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def put(self, request, pk=None):
        try:
            item = RecipeIngredient.objects.get(pk=pk)
            serializer = EditRecipeIngredientSerializer(
                item, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Recipe Ingredient updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "status": False,
                    "message": "Something went wrong",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Recipe Ingredient not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            item = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(item)
            return Response(
                {
                    "status": True,
                    "message": "Recipe Ingredient retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Recipe Ingredient not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            item = RecipeIngredient.objects.get(pk=pk)
            item.delete()
            return Response(
                {
                    "status": True,
                    "message": "Recipe Ingredient deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Recipe Ingredient not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    CommonIngredientsViewSet    --------------------


class CommonIngredientsViewSet(generics.GenericAPIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_recipe_for_item(self, item_name):
        """
        Efficiently retrieve recipe ingredients for a given item.

        Args:
            item_name (str): Name of the item to find recipe for.

        Returns:
            dict/list/None: Ingredients for the item or None if not found.
        """
        try:
            return (
                RecipeIngredient.objects.select_related("item")
                .get(item__name=item_name)
                .ingredients
            )
        except RecipeIngredient.DoesNotExist:
            return None

    def post(self, request):
        """
        Process event ingredients analysis.

        Args:
            request: HTTP request object.

        Returns:
            Response: JSON response with ingredient analysis.
        """
        # Validate event ID
        event_id = request.data.get("event_id")
        if not event_id:
            return Response(
                {"status": False, "message": "Event ID is required"},
                status=status.HTTP_200_OK,
            )

        # Fetch event
        try:
            event = EventBooking.objects.get(id=event_id)
        except EventBooking.DoesNotExist:
            return Response(
                {"status": False, "message": "Event not found"},
                status=status.HTTP_200_OK,
            )

        try:
            # Collect selected dishes directly from the JSONField
            selected_dishes = [
                {"item": item["name"], "item_category": category}
                for category, category_items in event.selected_items.items()
                for item in category_items
            ]

            # Optimize recipe ingredient retrieval
            item_names = [dish["item"] for dish in selected_dishes]
            recipe_ingredients = {
                ri.item.name: ri.ingredients
                for ri in RecipeIngredient.objects.select_related("item").filter(
                    item__name__in=item_names
                )
            }

            # Process ingredients more efficiently
            ingredient_to_dishes = defaultdict(list)
            for dish in selected_dishes:
                ingredients = recipe_ingredients.get(dish["item"])
                if ingredients:
                    if isinstance(ingredients, list):
                        for ingredient in ingredients:
                            ingredient_to_dishes[ingredient].append(
                                {
                                    "item_name": dish["item"],
                                    "item_category": dish["item_category"],
                                    "quantity": "",
                                }
                            )
                    elif isinstance(ingredients, dict):
                        for ingredient, quantity in ingredients.items():
                            ingredient_to_dishes[ingredient].append(
                                {
                                    "item_name": dish["item"],
                                    "item_category": dish["item_category"],
                                    "quantity": quantity,
                                }
                            )

            # Bulk fetch ingredient categories
            ingredient_categories = {
                item["name"]: data["name"]
                for data in IngridientsCategorySerializer(
                    IngridientsCategory.objects.all(), many=True
                ).data
                for item in data.get("items", [])
            }

            # Prepare response data with efficient category mapping
            response_data = defaultdict(list)

            for ingredient, dishes in ingredient_to_dishes.items():
                response_data[ingredient_categories.get(ingredient, "Other")].append(
                    {
                        "item": ingredient,
                        "quantity_type": "",
                        "use_item": dishes,
                        "total_quantity": "0",
                    }
                )

            # Add remaining uncategorized ingredients
            uncategorized = set(ingredient_categories.keys()) - set(
                ingredient_to_dishes.keys()
            )
            for ingredient in uncategorized:
                response_data[ingredient_categories.get(ingredient, "Other")].append(
                    {
                        "item": ingredient,
                        "quantity_type": "",
                        "use_item": [
                            {
                                "item_name": ingredient,
                                "item_category": ingredient_categories.get(
                                    ingredient, ""
                                ),
                                "quantity": "",
                            }
                        ],
                        "total_quantity": "0",
                    }
                )

            return Response(
                {
                    "status": True,
                    "message": "Ingredients analysis completed",
                    "data": [response_data],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_200_OK
            )
