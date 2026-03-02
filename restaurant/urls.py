from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_id>/', views.order_confirmed, name='order_confirmed'),
    
    # Staff views (require login)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/menu/', views.menu_management, name='menu_management'),
    path('dashboard/kitchen/', views.kitchen_view, name='kitchen_view'),
    path('dashboard/order/update/', views.update_order_status, name='update_order_status'),
    path('dashboard/dish/add/', views.add_dish, name='add_dish'),
    path('dashboard/category/add/', views.add_category, name='add_category'),
    path('dashboard/dish/<int:dish_id>/edit/', views.edit_dish, name='edit_dish'),
    path('dashboard/dish/<int:dish_id>/delete/', views.delete_dish, name='delete_dish'),
    path('dashboard/order/delete/', views.delete_order, name='delete_order'),
]
