from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import Response

from .models import MenuItem
from .serializers import MenuItemSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def menu_list(request, format=None):
    """ 
    List all menu items or create a new one
    """
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def menu_detail(request, pk, format=None):
    """ 
    Retrieve, update or delete a menu item.
    """
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Handles GET method
    if request.method == 'GET':
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    # Handles PUT method
    elif request.method == 'PUT':
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles DELETE method
    elif request.method == 'DELETE':
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuItemStaffList(generics.ListCreateAPIView):
    """
        List all menu items, or create a new menu item.
        Only for staff workers / managers etc.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# for customers / couriers
class MenuItemList(generics.ListAPIView):
    """
        List all menu items, or create a new menu item.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


#  for staff workers / managers etc.
class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a menu item instance.
        Only for staff workers / managers etc.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
