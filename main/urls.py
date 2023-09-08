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
    
    # manager
    path('staff/login/', views.managerLogin, name='manager_login'),
    path('staff/logout/', views.managerLogout, name='manager_logout'),
    path('staff/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('staff/profile/', views.manager_profile, name='manager_profile'),
    path('staff/stock/product_caterories/', views.manager_productCategory, name='manager_productCategory'),
    path('staff/stock/product_caterories/<int:pk>/category_details/', views.manager_categoryDetails, name='manager_categoryDetails'),
    path('staff/stock/products/', views.manager_product, name='manager_product'),
    path('staff/stock/products/<int:pk>/product_details/', views.manager_productDetails, name='manager_productDetails'),
    path('staff/stock/inventory/', views.manager_inventory, name='manager_inventory'),
    path('staff/clients/our_clients/', views.manager_clientList, name='manager_clientList'),
    path('staff/clients/our_clients/<int:pk>/client_profile/', views.manager_clientDetails, name='manager_clientDetails'),
    path('staff/clients/new_orders/', views.manager_newOrder, name='manager_newOrder'),
    path('staff/clients/new_orders/<int:pk>/order_details/', views.manager_newOrderDetails, name='manager_newOrderDetails'),
    path('staff/clients/archieved_orders/', views.manager_archieviedOrder, name='manager_archieviedOrder'),
    path('staff/clients/archieved_orders/<int:pk>/order_details/', views.manager_archievedOrderDetails, name='manager_archievedOrderDetails'),
    path('staff/clients/new_commands/', views.manager_newCommands, name='manager_newCommands'),
    path('staff/clients/new_commands/<int:pk>/command_details/', views.manager_newCommandDetails, name='manager_newCommandDetails'), 
    path('staff/clients/completed_commands/', views.manager_completedCommands, name='manager_completedCommands'),
    path('staff/clients/completed_commands/<int:pk>/command_details/', views.manager_completedCommandDetails, name='manager_completedCommandDetails'), 
]