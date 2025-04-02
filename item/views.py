from collections import defaultdict
import json
from rest_framework.response import Response
from rest_framework import status, generics
from ListOfIngridients.models import EventIngridientList, IngridientsCategory
from ListOfIngridients.serializers import IngridientsCategorySerializer
from Radhika.Utils.permissions import *
from eventbooking.models import EventBooking
from stockmanagement.models import StokeItem
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

    def consolidate_categories(self, data):
        # Create a dictionary to store merged categories
        consolidated = {}

        # Process each category
        for category in data:
            name = category["name"]

            # If this category name already exists in our consolidated dict
            if name in consolidated:
                # Extend the existing data with new items
                consolidated[name]["data"].extend(category["data"])
            else:
                # Create a new entry
                consolidated[name] = {"name": name, "data": category["data"].copy()}

        # Remove duplicate items within each category
        for name, category in consolidated.items():
            # Use a set to track unique items by their 'item' value
            unique_items = {}
            unique_data = []

            for item in category["data"]:
                item_name = item["item"]

                if item_name not in unique_items:
                    unique_items[item_name] = item
                    unique_data.append(item)
                else:
                    # If we encounter a duplicate item, merge the 'use_item' lists
                    existing = unique_items[item_name]

                    # Get unique use_items from both
                    existing_use_items = {
                        tuple(sorted(ui.items())) for ui in existing["use_item"]
                    }

                    for ui in item["use_item"]:
                        ui_tuple = tuple(sorted(ui.items()))
                        if ui_tuple not in existing_use_items:
                            existing["use_item"].append(ui)
                            existing_use_items.add(ui_tuple)

            # Update the category with deduplicated items
            category["data"] = unique_data

        # Convert back to list format
        result = list(consolidated.values())

        return result

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
        if EventIngridientList.objects.filter(event_id=event_id).exists():
            print("if")
            event_ingridient_list = EventIngridientList.objects.get(event_id=event_id)
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
                response_data = defaultdict(list)

                for ingredient, dishes in ingredient_to_dishes.items():
                    stoke_item = StokeItem.objects.filter(name=ingredient).first()
                    stoke_item_quantity = str(stoke_item.quantity) if stoke_item else ""
                    stoke_item_quantity_type = stoke_item.type if stoke_item else ""
                    response_data[
                        ingredient_categories.get(ingredient, "Other")
                    ].append(
                        {
                            "item": ingredient,
                            "quantity_type": "",
                            "godown_quantity": stoke_item_quantity,
                            "godown_quantity_type": stoke_item_quantity_type,
                            "use_item": dishes,
                            "total_quantity": "0",
                        }
                    )

                formatted_response = [
                    {"name": category, "data": items}
                    for category, items in response_data.items()
                ]
                new_list = (
                    event_ingridient_list.ingridient_list_data + formatted_response
                )
                
                unique_list = self.consolidate_categories(new_list)
                ___, ____ = EventIngridientList.objects.update_or_create(
                    event_id=event_id, defaults={"ingridient_list_data": unique_list}
                )
                return Response(
                    {
                        "status": True,
                        "message": "Ingredients analysis completed",
                        "data": unique_list,
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)}, status=status.HTTP_200_OK
                )

        else:
            print("else")
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
                    stoke_item = StokeItem.objects.filter(name=ingredient).first()
                    stoke_item_quantity = str(stoke_item.quantity) if stoke_item else ""
                    stoke_item_quantity_type = stoke_item.type if stoke_item else ""
                    response_data[
                        ingredient_categories.get(ingredient, "Other")
                    ].append(
                        {
                            "item": ingredient,
                            "quantity_type": "",
                            "godown_quantity": stoke_item_quantity,
                            "godown_quantity_type": stoke_item_quantity_type,
                            "use_item": dishes,
                            "total_quantity": "0",
                        }
                    )

                formatted_response = [
                    {"name": category, "data": items}
                    for category, items in response_data.items()
                ]

                event_ingridient_list, ____ = (
                    EventIngridientList.objects.update_or_create(
                        event_id=event_id,
                        defaults={"ingridient_list_data": formatted_response},
                    )
                )
                return Response(
                    {
                        "status": True,
                        "message": "Ingredients analysis completed",
                        "data": formatted_response,
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)}, status=status.HTTP_200_OK
                )
