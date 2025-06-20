from django.urls import path
from .views import MenuItemView,SingleItemView ,manager,CartMenuItemsView,OrdersView,SingleOrderView,AdminOrdersView,SingCartView,DeliveryCrewView,DestroyMenuItemsView
urlpatterns = [
    path('menu-items/' ,MenuItemView.as_view()),
    path('menu-items/<int:pk>' ,SingleItemView.as_view()),
    path('groups/manager/users/',manager),
    path('groups/delivery-crew/users', DeliveryCrewView.as_view(), name='delivery-crew-users'),
    path('groups/delivery-crew/user', DestroyMenuItemsView.as_view()),
    path('orders/', OrdersView.as_view()),
    path('order/', AdminOrdersView.as_view()),
    path('orders/<int:pk>', SingleOrderView.as_view()),
    path('cart/menu-items/', CartMenuItemsView.as_view(), name='cart-menu-items'),
    path('cart/menu-items/<int:pk>', SingCartView.as_view(), name='cart-menu-items'),
    
]
