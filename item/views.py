from collections import defaultdict
from rest_framework.response import Response
from rest_framework import status, generics
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
        used_item_ids = set(RecipeIngredient.objects.values_list('item__pk', flat=True))

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
            serializer = ItemSerializer(item, data=request.data)
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
        serializer = RecipeIngredientSerializer(recipe_ingredient,many=True)
        for data in serializer.data:
            item = Item.objects.filter(pk = data.get("item")).values("name").first()
            data['item'] = item
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
            serializer = EditRecipeIngredientSerializer(item, data=request.data)
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


# --------------------    CommonIngredientsView    --------------------


class CommonIngredientsView(generics.GenericAPIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_recipe_for_item(self, item_name):
        try:
            item = Item.objects.get(name=item_name)
            recipe = RecipeIngredient.objects.get(item=item)
            return recipe.ingredients
        except (Item.DoesNotExist, RecipeIngredient.DoesNotExist):
            return None

    def post(self, request):
        try:
            # Get event booking ID from request
            event_id = request.data.get('event_id')
            if not event_id:
                return Response({
                    'status': False,
                    'message': 'Event ID is required'
                }, status=status.HTTP_200_OK)

            # Get event booking
            try:
                event = EventBooking.objects.get(id=event_id)
            except EventBooking.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'Event not found'
                }, status=status.HTTP_200_OK)

            # Get all selected items from the event
            selected_dishes = []
            for category_items in event.selected_items.values():
                for item in category_items:
                    selected_dishes.append(item['name'])

            # Get recipes and organize ingredients
            ingredient_to_dishes = defaultdict(list)
            ingredient_frequency = defaultdict(int)
            
            # First pass: collect all ingredients and count their frequency
            for dish_name in selected_dishes:
                ingredients = self.get_recipe_for_item(dish_name)
                if ingredients:
                    # Handle both list and dict type ingredients
                    if isinstance(ingredients, list):
                        for ingredient in ingredients:
                            ingredient_to_dishes[ingredient].append({
                                'item_name': dish_name,
                                'quantity': ''
                            })
                            ingredient_frequency[ingredient] += 1
                    elif isinstance(ingredients, dict):
                        for ingredient in ingredients.keys():
                            ingredient_to_dishes[ingredient].append({
                                'item_name': dish_name,
                                'quantity': ingredients.get(ingredient, '')
                            })
                            ingredient_frequency[ingredient] += 1

            # Format response and sort by frequency
            response_data = []
            sorted_ingredients = sorted(
                ingredient_to_dishes.items(),
                key=lambda x: (-ingredient_frequency[x[0]], x[0])  # Sort by frequency desc, then name asc
            )

            for ingredient, using_dishes in sorted_ingredients:
                ingredient_data = {
                    'item': ingredient,
                    'frequency': ingredient_frequency[ingredient],  # Added frequency count
                    'quantity_type': '',
                    'use_item': using_dishes,
                    'total_quantity': '0',
                    'is_common': ingredient_frequency[ingredient] > 1  # Flag for common ingredients
                }
                response_data.append(ingredient_data)

            return Response({
                'status': True,
                'message': 'Ingredients analysis completed',
                'data': response_data,
                'summary': {
                    'total_ingredients': len(response_data),
                    'common_ingredients': sum(1 for item in response_data if item['is_common'])
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_200_OK)
