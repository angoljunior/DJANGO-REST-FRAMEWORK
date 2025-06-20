from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from .models import MenuItem,Order,OrderItem,Category,Cart
from rest_framework.decorators import api_view, renderer_classes,throttle_classes,permission_classes ,APIView
from .serializers import MenuItemSerializer,CartSerializer,OrderSerializer,UserSerializer
from django.contrib.auth.models import User,Group

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    queryset         =  MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['price','inventory','title']
    ordering_fields = ['price','inventory','title']

class SingleItemView(generics.RetrieveAPIView ,generics.DestroyAPIView):
    queryset         =  MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['POST','GET','DELETE'])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User ,username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({'message': 'User successfully Added to Managers'})

        #Deleting user from the model
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({'message': 'User successfully Deleted'})
        
    return Response({'message': 'ok'} ,status.HTTP_200_OK)



@permission_classes([IsAuthenticated])
class CartMenuItemsView(generics.ListCreateAPIView ,generics.DestroyAPIView):
    queryset         = Cart.objects.all()
    serializer_class = CartSerializer

    def delete(self, request):
        # Fetch all cart items for the current user
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # Delete the items
        cart_items.delete()

        return Response({'message': 'All cart items deleted successfully.'}, status=status.HTTP_200_OK)


class SingCartView(generics.RetrieveUpdateAPIView):
    queryset         = Cart.objects.all()
    serializer_class = CartSerializer


@permission_classes([IsAuthenticated])
class OrdersView(generics.ListCreateAPIView):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer

@permission_classes([IsAdminUser])
class AdminOrdersView(generics.ListAPIView):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer

@permission_classes([IsAdminUser])
class SingleOrderView(generics.RetrieveAPIView,generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer


class DeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the "delivery-crew" group
            group = Group.objects.get(name="delivery-crew")
            # Retrieve all users in the group
            delivery_crew_users = group.user_set.all()
            
            # Serialize the user data (basic example, you might want a custom serializer)
            data = [
                {"id": user.id, "username": user.username, "email": user.email}
                for user in delivery_crew_users
            ]
            return Response(data, status=200)
        except Group.DoesNotExist:
            return Response({"error": "Delivery crew group not found."}, status=404)


@permission_classes([IsAuthenticated])
class DestroyMenuItemsView(generics.DestroyAPIView,generics.ListCreateAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request):
        # Fetch all cart items for the current user
        user = request.user
        cart_items = Group.objects.filter(user=user)

        # Delete the items
        cart_items.delete()

        return Response({'message': 'All delivery crew items deleted successfully.'}, status=status.HTTP_200_OK)
