from django.urls import path
from main import views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/about/', views.about, name='about'),
    path('shop/contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<str:name>/', views.shopCategory, name='shop_category'),
    path('shop/search/', views.search_result, name='search_result'),
    path('shop/search/<str:search_data>/', views.search_result, name='search_result'),
    path('shop/product/<int:pk>/product_details/', views.product_details, name='product_details'),
    # cart urls
    path('shop/cart/', views.shop_cart, name='shop_cart'),
    path('shop/cart/add_to_cart/<int:product_id>/', views.addToCart, name='add_to_cart'),
    path('shop/cart/update_cart/', views.updateCart, name='update_cart'),
    path('shop/cart/remove_from_cart/<int:product_id>/', views.removeFromCart, name='remove_from_cart'),

    path('shop/checkout/', views.shop_checkout, name='shop_checkout'),
    path('shop/order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('shop/client/login/', views.client_login, name='client_login'),
    path('shop/client/register/', views.client_register, name='client_register'),
    path('shop/client/logout/', views.client_logout, name='client_logout'),
    path('shop/client/dashboard/', views.client_dashboard, name='client_account'),
    path('shop/client/profile/', views.client_profile, name='client_profile'),
    path('shop/client/order_list/', views.client_order_list, name='client_order_list'),
    path('shop/client/order_list/<int:pk>/', views.client_order_details, name='client_order_details'),
]
