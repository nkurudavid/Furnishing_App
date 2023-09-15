from django.urls import path
from main import views


urlpatterns = [
    #     path('', views.home, name='home'),
    #     path('shop/about/', views.about, name='about'),
    #     path('shop/contact/', views.contact, name='contact'),
    #     path('shop/', views.shop, name='shop'),
    #     path('shop/category/<str:name>/', views.shopCategory, name='shop_category'),
    #     path('shop/search/', views.search_result, name='search_result'),
    #     path('shop/search/<str:search_data>/',
    #          views.search_result, name='search_result'),
    #     path('shop/product/<int:pk>/product_details/',
    #          views.product_details, name='product_details'),
    #     # cart urls
    #     path('shop/cart/', views.shop_cart, name='shop_cart'),
    #     path('shop/cart/add_to_cart/<int:product_id>/',
    #          views.addToCart, name='add_to_cart'),
    #     path('shop/cart/update_cart/', views.updateCart, name='update_cart'),
    #     path('shop/cart/remove_from_cart/<int:product_id>/',
    #          views.removeFromCart, name='remove_from_cart'),

    #     path('shop/checkout/', views.shop_checkout, name='shop_checkout'),
    #     path('shop/order_confirmation/',
    #          views.order_confirmation, name='order_confirmation'),
    #     path('shop/client/login/', views.client_login, name='client_login'),
    #     path('shop/client/register/', views.client_register, name='client_register'),
    #     path('shop/client/logout/', views.client_logout, name='client_logout'),
    #     path('shop/client/dashboard/', views.client_dashboard, name='client_account'),
    #     path('shop/client/profile/', views.client_profile, name='client_profile'),
    #     path('shop/client/order_list/',
    #          views.client_order_list, name='client_order_list'),
    #     path('shop/client/order_list/<int:pk>/',
    #          views.client_order_details, name='client_order_details'),

    # manager urls
    path('staff/login/', views.staffLogin, name='staffLogin'),
    path('staff/logout/', views.staffLogout, name='staffLogout'),
    path('staff/manager/dashboard/',
         views.manager_dashboard, name='manager_dashboard'),
    path('staff/manager/profile/', views.manager_profile, name='manager_profile'),
    path('staff/manager/staffmember/',
         views.manager_craftsmanList, name='manager_craftsmanList'),
    path('staff/manager/staffmember/<int:pk>/craftsman_profile/',
         views.manager_craftsmanDetails, name='manager_craftsmanDetails'),
    path('staff/manager/stock/product_caterories/',
         views.manager_productCategory, name='manager_productCategory'),
    path('staff/manager/stock/product_caterories/<int:pk>/category_details/',
         views.manager_categoryDetails, name='manager_categoryDetails'),
    path('staff/manager/stock/products/',
         views.manager_product, name='manager_product'),
    path('staff/manager/stock/products/<int:pk>/product_details/',
         views.manager_productDetails, name='manager_productDetails'),
    path('staff/manager/stock/materials/', views.manager_materials,
         name='manager_materials'),
    path('staff/manager/stock/materials/<int:pk>/material_details/',
         views.manager_materialDetails, name='manager_materialDetails'),
    path('staff/manager/stock/inventory/', views.manager_inventory,
         name='manager_inventory'),
    path('staff/manager/clients/our_clients/',
         views.manager_clientList, name='manager_clientList'),
    path('staff/manager/clients/our_clients/<int:pk>/client_profile/',
         views.manager_clientDetails, name='manager_clientDetails'),
    path('staff/manager/clients/new_orders/',
         views.manager_newOrder, name='manager_newOrder'),
    path('staff/manager/clients/new_orders/<int:pk>/order_details/',
         views.manager_newOrderDetails, name='manager_newOrderDetails'),
    path('staff/manager/clients/archieved_orders/',
         views.manager_archieviedOrder, name='manager_archieviedOrder'),
    path('staff/manager/clients/archieved_orders/<int:pk>/order_details/',
         views.manager_archievedOrderDetails, name='manager_archievedOrderDetails'),
    path('staff/manager/clients/new_custom_orders/',
         views.manager_newCustomOrders, name='manager_newCustomOrders'),
    path('staff/manager/clients/new_custom_orders/<int:pk>/costom_order_details/',
         views.manager_newCustomOrderDetails, name='manager_newCustomOrderDetails'),
    path('staff/manager/clients/completed_custom_orders/',
         views.manager_completedCustomOrders, name='manager_completedCustomOrders'),
    path('staff/manager/clients/completed_custom_orders/<int:pk>/costom_order_details/',
         views.manager_completedCustomOrderDetails, name='manager_completedCustomOrderDetails'),

    # Craftsman urls
    path('staff/craftsman/dashboard/',
         views.craftsman_dashboard, name='craftsman_dashboard'),
    path('staff/craftsman/profile/',
         views.craftsman_profile, name='craftsman_profile'),
]
