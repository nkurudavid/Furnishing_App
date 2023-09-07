import random
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash

from django.db.models import Q

from main.models import *
from account.models import ClientProfile


# my functions
def search_products_filter(search_data=None):
    if search_data:
        # get data where category name contains search_data or product name contains search_data
        matched_products = Product.objects.filter(Q(category__category_name__icontains=search_data) | Q(product_name__icontains=search_data))
    return matched_products



# Create your views here.
def handle_not_found(request, exception):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        context = {
            'title': 'Page Not found',
        }
        return render(request, 'main/404.html', context)



def home(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        categories = ProductCategory.objects.filter()
        selected_products = []

        for category in categories:
            product = Product.objects.filter(category=category).first()
            if product:
                selected_products.append(product)

        selected_products = selected_products[:6]
        context = {
            'title': 'Welcome',
            'categories': categories,
            'products': selected_products,
        }
        return render(request, 'main/home.html', context)



def about(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        context = {
            'title': 'About us',
        }
        return render(request, 'main/about.html', context)



def contact(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        context = {
            'title': 'Contact us',
        }
        return render(request, 'main/contact.html', context)



def shop(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        categories = ProductCategory.objects.filter()
        products = Product.objects.filter()
        context = {
            'title': 'Shop',
            'categories': categories,
            'products': products,
        }
        return render(request, 'main/shop.html', context)



def search_result(request, search_data=None):
    if search_data:
        # Call the search_products_filter function to get the filtered products
        filtered_products = search_products_filter(search_data)

        categoryData = ProductCategory.objects.filter()
        context = {
            'title': 'Shop - Search Result',
            'categories': categoryData,
            'products': filtered_products,
        }
        return render(request, 'main/search_result.html', context)
    else:
        return redirect(shop)



def shopCategory(request, name):
    category_name = name
    # check if category exist
    if ProductCategory.objects.filter(category_name=category_name).exists():
        # if exists
        selectedCategory = ProductCategory.objects.get(category_name=category_name)
        products = Product.objects.filter(category=selectedCategory)

        if 'search' in request.POST:
            search_data = request.POST.get("search_data")

            if search_data:
                # Call the search_result function and pass the data
                return search_result(request, search_data)
            else:
                return redirect(shop)
        else:
            categories = ProductCategory.objects.filter()
            context = {
                'title': 'Shop - category',
                'categories': categories,
                'products': products,
                'selectedCategory': selectedCategory,
            }
            return render(request, 'main/shop.html', context)
    else:
        messages.error(request, ('Product Category not found'))
        return redirect(shop)




def product_details(request, pk):
    product_id = pk
    # check if category exist
    if Product.objects.filter(id=product_id).exists():
        # if exists
        selected_product = Product.objects.get(id=product_id)

        if 'search' in request.POST:
            search_data = request.POST.get("search_data")

            if search_data:
                # Call the search_result function and pass the data
                return search_result(request, search_data)
            else:
                return redirect(shop)
        else:
            categories = ProductCategory.objects.filter()
            context = {
                'title': 'Shop - Product details',
                'categories': categories,
                'p_data': selected_product,
            }
            return render(request, 'main/product_details.html', context)
    else:
        messages.error(request, ('Product not found'))
        return redirect(shop)



def shop_cart(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        # get data from cart
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0
        for product_id, item in cart.items():
            p_data = Product.objects.get(id=int(product_id))
            item['p_data'] = p_data
            item['subtotal'] = p_data.price * item['quantity']
            total_price += item['subtotal']
            cart_items.append(item)

        else:
            # return the value to template
            context ={
                'title': 'Shop - Cart',
                'cart_items': cart_items,
                'total_price': total_price,
            }
            return render(request, 'main/shop_cart.html', context)



def addToCart(request, product_id):
    # get quantity is provided
    if request.POST.get('qty'):
        quantity = int(request.POST.get('qty'))
    else:
        quantity = 1

    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id), {'quantity': 0})
    cart_item['quantity'] += quantity
    cart[str(product_id)] = cart_item
    request.session['cart'] = cart
    return redirect(shop_cart)


def updateCart(request):
    # update cart values
    if 'update_cart' in request.POST:
        cart = request.session.get('cart', {})
        for product_id, quantity in request.POST.items():
            if product_id.startswith('quantity_'):
                product_id = product_id.split('_')[1]
                cart_item = cart.get(str(product_id), {'quantity': 0})
                cart_item['quantity'] = int(quantity)
                cart[str(product_id)] = cart_item
        request.session['cart'] = cart
    return redirect(shop_cart)



def removeFromCart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect(shop_cart)




@login_required(login_url='shop')
def shop_checkout(request):
    if request.user.is_authenticated and request.user.is_client==True:
        if 'search' in request.POST:
            search_data = request.POST.get("search_data")
            if search_data:
                # Call the search_result function and pass the data
                return search_result(request, search_data)
            else:
                return redirect(shop)
        else:
            return render(request, 'main/checkout.html')
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)



@login_required(login_url='shop')
def order_confirmation(request):
    if request.user.is_authenticated and request.user.is_client==True:
        if 'place_order' in request.POST:
            shipping_location = request.POST.get("shipping_location")
            shipping_street = request.POST.get("shipping_street")
            pay_method = request.POST.get("pay_method")
            payment_id = request.POST.get("payment_id")

            # Generate a random number for order number
            order_no = random.randint(1, 1000000)

            # get data from cart to get total_amount
            cart = request.session.get('cart', {})
            total_price = 0
            for product_id, item in cart.items():
                p_data = Product.objects.get(id=int(product_id))
                total_price += p_data.price * item['quantity']

            # add new order
            client_order = Order(
                client = get_user_model().objects.get(email=request.user.email),
                order_number =order_no,
                status = 'Pending',
                shipping_address = shipping_location+"/ "+shipping_street,
                total_amount = total_price,
                payment_method = pay_method,
                payment_id = payment_id,
            )
            client_order.save()
            if client_order:
                for product_id, item in cart.items():
                    details = OrderDetail(
                        order = client_order,
                        product = Product.objects.get(id=int(product_id)),
                        quantity = item['quantity'],
                    )
                    details.save()

            # Clear the cart after order submission
            request.session['cart'] = {}
            messages.success(request, ('Your order is on waiting list!'))
            return redirect(client_order_list)
        else:
            messages.success(request, ('Oops! error in placing order.'))
            return redirect(shop_checkout)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop_checkout)




def client_login(request):
    if not request.user.is_authenticated or request.user.is_client!=True:
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_client==True:
                login(request, user)
                messages.success(request, ('Hi '+user.first_name+', you are logged in'))
                return redirect(client_dashboard)
            else:
                messages.error(request, ('User Email or Password is not correct! Try agin...'))
                return redirect(shop)
    else:
        return redirect(client_dashboard)




def client_register(request):
    if not request.user.is_authenticated or request.user.is_client!=True:
        if 'sign_up' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            phone_number = request.POST.get('phone_number')
            location = request.POST.get('location')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if first_name and last_name and gender and phone_number and location and email and password1 and password2:
                if get_user_model().objects.filter(email=email).exists():
                    messages.error(request, ('Email address already taken'))
                    return redirect(home)
                if password1 and password2 and password1 != password2:
                    messages.error(request, ('Passwords do not match'))
                    return redirect(home)
                else:
                    # Create a new user object with the submitted data
                    user = get_user_model().objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        is_client=True,
                        email=email,
                        password=password1,
                    )
                    if user:
                        # get client account
                        client = get_user_model().objects.get(email=email)
                        # get client profile
                        client_profile, created = ClientProfile.objects.get_or_create(client=client)

                        # update client profile and save
                        client_profile.phone_number=phone_number
                        client_profile.location=location
                        client_profile.save()

                    user = authenticate(request, email=email, password=password1)
                    if user is not None and user.is_client==True:
                        login(request, user)
                        messages.success(request, ('Hi '+user.first_name+', you are logged in'))
                        return redirect(client_dashboard)
            else:
                messages.error(request, ('All field are required'))
                return redirect(shop)
    else:
        return redirect(client_dashboard)




@login_required(login_url='shop')
def client_logout(request):
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(shop)




@login_required(login_url='shop')
def client_dashboard(request):
    if request.user.is_authenticated and request.user.is_client==True:
        # client orders
        orders = Order.objects.filter(client=request.user)
        new_orders = Order.objects.filter(client=request.user).exclude(status='Success').count()
        context = {
            'title': 'Client Account',
            'orders': orders,
            'new_orders': new_orders,
            'dashboard_active': 'active',
        }
        return render(request, 'main/client_account.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)



@login_required(login_url='shop')
def client_order_list(request):
    if request.user.is_authenticated and request.user.is_client==True:
        # client orders
        orders = Order.objects.filter(client=request.user).order_by('-created_date','status')
        new_orders = Order.objects.filter(client=request.user).exclude(status='Success').count()
        context = {
            'title': 'Client Account',
            'orders': orders,
            'new_orders': new_orders,
            'orders_active': 'active',
        }
        return render(request, 'main/client_order_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)




@login_required(login_url='shop')
def client_order_details(request, pk):
    if request.user.is_authenticated and request.user.is_client==True:
        order_id = pk
        if Order.objects.filter(client=request.user, pk=order_id).exists():
            # client orders
            order = Order.objects.get(client=request.user, pk=order_id)
            new_orders = Order.objects.filter(client=request.user).exclude(status='Success').count()
            context = {
                'title': 'Client Account',
                'order': order,
                'new_orders': new_orders,
                'orders_active': 'active',
            }
            return render(request, 'main/client_order_details.html', context)
        else:
            messages.warning(request, ('Order not found'))
            return redirect(client_order_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)




@login_required(login_url='shop')
def client_profile(request):
    if request.user.is_authenticated and request.user.is_client==True:
        if 'update_profile' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            phone_number = request.POST.get('phone_number')
            location = request.POST.get('location')

            if first_name and last_name and gender and phone_number and location:
                # get client account
                get_user_model().objects.filter(email=request.user.email).update(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                )

                # get client profile
                c_profile, created = ClientProfile.objects.get_or_create(client=get_user_model().objects.get(email=request.user.email))

                # update client profile and save
                c_profile.phone_number=phone_number
                c_profile.location=location
                c_profile.save()

                messages.success(request, ('Profile updated successfully'))
                return redirect(client_profile)
            else:
                messages.error(request, ('All field are required'))
                return redirect(client_profile)

        elif 'update_shipping_address' in request.POST:
            shipping_location = request.POST.get('shipping_location')
            shipping_street = request.POST.get('shipping_street')

            if shipping_location and shipping_street:
                # get client profile
                c_profile, created = ClientProfile.objects.get_or_create(client=get_user_model().objects.get(email=request.user.email))

                # update client shipping address and save
                c_profile.shipping_location=shipping_location
                c_profile.shipping_street=shipping_street
                c_profile.save()

                messages.success(request, ('Shipping address updated successfully'))
                return redirect(client_profile)
            else:
                messages.error(request, ('All field are required'))
                return redirect(client_profile)

        elif 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)
                if not user.check_password(old_password):
                    messages.error(request, "Your old password is not correct!")
                    return redirect(client_profile)
                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(client_profile)
                    elif new_password != confirmed_new_password:
                        messages.error(request, "Your new password not match the confirm password !")
                        return redirect(client_profile)
                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(request, "Your password has been changed successfully.!")
                        return redirect(client_profile)
            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(client_profile)
        else:
            new_orders = Order.objects.filter(client=request.user).exclude(status='Success').count()
            context = {
                'title': 'Client Profile',
                'new_orders': new_orders,
                'profile_active': 'active',
            }
            return render(request, 'main/client_profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)
    
    
    
    
    
    
    
    # staff
    
    
    

def managerLogin(request,):
    if not request.user.is_authenticated or request.user.is_manager != True:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_manager == True:
                login(request, user)
                messages.success(
                    request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(manager_dashboard)
            else:
                messages.error(
                    request, ('User Email or Password is not correct! Try agin...'))
                return redirect(managerLogin)
        else:
            context = {'title': 'Management Login', }
            return render(request, 'main/dashboard/login.html', context)
    else:
        return redirect(manager_dashboard)



@login_required(login_url='manager_login')
def managerLogout(request):
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_dashboard(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        clients = ClientProfile.objects.filter()
        orders_data = Order.objects.filter().exclude(status="Success").order_by('status','created_date')[:10]

        context = {
            'title': 'Management - Dashboard',
            'dash_active': 'active',
            'clients': clients,
            'orders_data': orders_data,
            'clients_count': clients.count(),
        }
        return render(request, 'main/dashboard/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_profile(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)

                if not user.check_password(old_password):
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(manager_profile)

                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(manager_profile)

                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(manager_profile)

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(manager_profile)

            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(manager_profile)

        else:
            orders_data = Order.objects.filter(status="Pending")
            context = {
                'title': 'Management - Profile',
                'orders_data': orders_data,
            }
            return render(request, 'main/dashboard/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_productCategory(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_pCategory' in request.POST:
            category_name = request.POST.get("category_name")

            if category_name:
                found_data = ProductCategory.objects.filter(category_name=category_name)
                if found_data:
                    messages.warning(request, "The product category "+category_name+", Already exist.")
                    return redirect(manager_productCategory)
                else:
                    # add new product category
                    addCategory = ProductCategory(
                        category_name=category_name,
                    )
                    addCategory.save()

                    messages.success(request, "New Product category created successfully.")
                    return redirect(manager_productCategory)
            else:
                messages.error(request, "Error , Category name is required!")
                return redirect(manager_productCategory)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting provinces
            categoryData = ProductCategory.objects.filter().order_by('category_name')
            context = {
                'title': 'Management - Product category List',
                'category_active': 'active',
                'categories': categoryData,
                # 'request_data': request_data,
            }
            return render(request, 'main/dashboard/product_category.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_categoryDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        category_id = pk
        # getting 
        if ProductCategory.objects.filter(id=category_id).exists():
            # if exists
            foundData = ProductCategory.objects.get(id=category_id)

            if 'update_category' in request.POST:
                # Retrieve the form data from the request
                category_name = request.POST.get('category_name')

                if category_name:
                    if ProductCategory.objects.filter(category_name=category_name).exclude(id=category_id):
                        messages.warning(
                            request, "Category name already exist.")
                        return redirect(manager_categoryDetails, pk)
                    else:
                        # Update product category
                        category_updated = ProductCategory.objects.filter(id=category_id).update(
                            category_name=category_name,
                        )
                        if category_updated:
                            messages.success(request, "Category "+category_name+", Updated successfully.")
                            return redirect(manager_categoryDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(manager_categoryDetails, pk)
                else:
                    messages.error(request, ('Category name is required.'))
                    return redirect(manager_categoryDetails, pk)

            elif 'delete_category' in request.POST:
                # Delete product category
                foundData.delete()
                messages.success(request, "Product category info deleted successfully.")
                return redirect(manager_productCategory)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                context = {
                    'title': 'Management - ProductCategory Info',
                    'category_active': 'active',
                    'category': foundData,
                    # 'request_data': request_data,
                }
                return render(request, 'main/dashboard/product_categoryDetails.html', context)
        else:
            messages.error(request, ('Product category not found'))
            return redirect(manager_productCategory)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)




@login_required(login_url='manager_login')
def manager_product(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_commune' in request.POST:
            category_id = request.Post.get("category")
            product_name = request.Post.get("product_name")
            description = request.Post.get("description")
            price = request.Post.get("price")
            color = request.Post.get("color")
            quantity = request.Post.get("quantity")
            picture = request.Post.get("picture")

            if category_id and product_name and description and price and color and quantity and picture:
                # check if existing product
                if Product.objects.filter(ProductCategory=category_id,product_name=product_name).exists():
                    messages.warning(request, "The product name " +product_name+", Already exist.")
                    return redirect(manager_product)
                else:
                    # add new product
                    addProduct = Product(
                        province=ProductCategory.objects.get(id=category_id),
                        product_name=product_name,
                        description=description,
                        price=price,
                        color=color,
                        quantity=quantity,
                        picture=picture,
                    )
                    addProduct.save()

                    messages.success(
                        request, "New product created successfully.")
                    return redirect(manager_product)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(manager_product)
        else:
            # request_data = Application.objects.filter(status="Waiting")
            # getting province
            categoriesData = ProductCategory.objects.filter().order_by('category_name')
            # getting communes
            productsData = Product.objects.filter().order_by('category','product_name')
            context = {
                'title': 'Management - Products List',
                'product_active': 'active',
                'categories': categoriesData,
                'products': productsData,
                # 'request_data': request_data,
            }
            return render(request, 'main/dashboard/product_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_productDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        product_id = pk
        # getting product
        if Product.objects.filter(id=product_id).exists():
            # if exists
            foundData = Product.objects.get(id=product_id)

            if 'update_product' in request.POST:
                # Retrieve the form data from the request
                category_id = request.Post.get("category")
                product_name = request.Post.get("product_name")
                description = request.Post.get("description")
                price = request.Post.get("price")
                color = request.Post.get("color")
                quantity = request.Post.get("quantity")

                if category_id and product_name and description and price and color and quantity:
                    if Product.objects.filter(ProductCategory=category_id,product_name=product_name).exclude(id=product_id).exists():
                        messages.warning(request, "Product name already exist.")
                        return redirect(manager_productDetails, pk)
                    else:
                        # Update product
                        productUpdated = Product.objects.filter(id=product_id).update(
                            province=ProductCategory.objects.get(id=category_id),
                            product_name=product_name,
                            description=description,
                            price=price,
                            color=color,
                            quantity=quantity,
                        )
                        if productUpdated:
                            messages.success(request, "Product "+product_name+", Updated successfully.")
                            return redirect(manager_productDetails, pk)
                        else:
                            messages.error(request, ('Process Failed.'))
                            return redirect(manager_productDetails, pk)
                else:
                    messages.error(request, ('Error!, All fields are required.'))
                    return redirect(manager_productDetails, pk)

            elif 'delete_product' in request.POST:
                # Delete product
                foundData.delete()
                messages.success(request, "Product info deleted successfully.")
                return redirect(manager_product)

            else:
                # request_data = Application.objects.filter(status="Waiting")
                
                # getting Product categories
                categoriesData = ProductCategory.objects.filter().order_by('category_name')
                context = {
                    'title': 'Management - Product Info',
                    'product_active': 'active',
                    'categories': categoriesData,
                    'product': foundData,
                    # 'request_data': request_data,
                }
                return render(request, 'main/dashboard/product_details.html', context)
        else:
            messages.error(request, ('Product not found'))
            return redirect(manager_product)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)




@login_required(login_url='manager_login')
def manager_clientList(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        clientsData = ClientProfile.objects.filter().order_by('client__first_name')
        context = {
            'title': 'Management - Clients List',
            'client_active': 'active',
            'clients': clientsData,
            # 'request_data': request_data,
        }
        return render(request, 'main/dashboard/client_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_clientDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        client_id = pk
        # getting client profile
        if ClientProfile.objects.filter(id=client_id).exists():
            # if exists
            foundData = ClientProfile.objects.get(id=client_id)

            # request_data = Application.objects.filter(status="Waiting")
            context = {
                'title': 'Management - Client Info',
                'client_active': 'active',
                'client': foundData,
                # 'request_data': request_data,
            }
            return render(request, 'main/dashboard/client_details.html', context)
        else:
            messages.error(request, ('Client info not found'))
            return redirect(manager_clientList)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_newOrder(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting new request
        orders_data = Order.objects.filter().exclude(status="Success").order_by('status','created_date')
        context = {
            'title': 'Management - New Orders',
            'order_active': 'open active',
            'newOrder_active': 'active',
            'orders_data': orders_data,
        }
        return render(request, 'main/dashboard/newOrder_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_newOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if Order.objects.filter(id=newOrder_id).exclude(status="Success").exists():
            clientOrder = Order.objects.get(id=newOrder_id)

            if 'take_action' in request.POST:
                # Retrieve the form data from the request
                action = request.Post.get("action")

                if action:
                    # update the status
                    Order.objects.filter(id=newOrder_id).exclude(status="Success").update(
                        status=action,
                    )
                    messages.success(request, "Order status updated successfully")
                    return redirect(manager_newOrderDetails, pk)
                else:
                    messages.error(request, "Make sure to select action on this order.")
                    return redirect(manager_newOrderDetails, pk)
            else:
                # getting new request
                newOrders = Order.objects.filter().exclude(status="Success")
                context = {
                    'title': 'Management - New order details',
                    'order_active': 'open active',
                    'newOrder_active': 'active',
                    'clientOrder': clientOrder,
                    'new_orders': newOrders,
                }
                return render(request, 'main/dashboard/new_orderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(manager_newOrder)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_archieviedOrder(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting new request
        orders_data = Order.objects.filter(status="Success").order_by('created_date')
        context = {
            'title': 'Management - Archieved Orders',
            'order_active': 'open active',
            'archievedOrder_active': 'active',
            'orders_data': orders_data,
        }
        return render(request, 'main/dashboard/archieved_orderList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



@login_required(login_url='manager_login')
def manager_archievedOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if Order.objects.filter(id=newOrder_id, status="Success").exists():
            clientOrder = Order.objects.get(id=newOrder_id, status="Success")

            if 'take_action' in request.POST:
                # Retrieve the form data from the request
                action = request.Post.get("action")

                if action:
                    # update the status
                    Order.objects.filter(id=newOrder_id, status="Success").update(
                        status=action,
                    )
                    messages.success(request, "Order status updated successfully")
                    return redirect(manager_archievedOrderDetails, pk)
                else:
                    messages.error(request, "Make sure to select action on this order.")
                    return redirect(manager_archievedOrderDetails, pk)
            else:
                # getting new request
                newOrders = Order.objects.filter().exclude(status="Success")
                context = {
                    'title': 'Management - Archieved order details',
                    'order_active': 'open active',
                    'archievedOrder_active': 'active',
                    'clientOrder': clientOrder,
                    'new_orders': newOrders,
                }
                return render(request, 'main/dashboard/archieved_orderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(manager_archieviedOrder)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(managerLogin)



# @login_required(login_url='manager_login')
# def archivedRequest(request,):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         request_data = Application.objects.filter(status="Waiting")
#         # getting archived requests
#         archivedRequests = Application.objects.exclude(status="Waiting")
#         context = {
#             'title': 'Registrar - Archived Document Requests',
#             'request_active': 'open active',
#             'archived_active': 'active',
#             'archivedRequests': archivedRequests,
#             'request_data': request_data,
#         }
#         return render(request, 'main/dashboard/archived_request.html', context)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)


# @login_required(login_url='manager_login')
# def archivedRequest_details(request, pk):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         archivedRequest_id = pk
#         if Application.objects.filter(id=archivedRequest_id).exclude(status="Waiting").exists():
#             # getting archived requests
#             archived_details = Application.objects.get(Q(id=archivedRequest_id) & ~Q(status="Waiting"))
#             request_data = Application.objects.filter(status="Waiting")

#             # getting document
#             if CitizenDocument.objects.filter(document_number=archived_details.document_number).exists():
#                 document = CitizenDocument.objects.get(
#                     document_number=archived_details.document_number).file
#             else:
#                 document = None

#             # get idd document is exist
#             if CitizenDocument.objects.filter(document="Individual Descriptive Document", citizen=archived_details.citizen).exists():
#                 idd_doc = CitizenDocument.objects.filter(
#                     document="Individual Descriptive Document", citizen=archived_details.citizen).last()
#             else:
#                 idd_doc = None

#                 # getting new request

#             context = {
#                 'title': 'Registrar - Archived Document Requests',
#                 'request_active': 'open active',
#                 'archived_active': 'active',
#                 'archived_details': archived_details,
#                 'request_data': request_data,
#                 'document': document,
#                 'idd_doc': idd_doc,
#             }
#             return render(request, 'main/dashboard/archived_details.html', context)
#         else:
#             messages.warning(request, ('request not found'))
#             return redirect(archivedRequest)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)


# @login_required(login_url='manager_login')
# def services(request):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         if 'new_service' in request.POST:
#             service_name = request.POST.get("service_name")
#             description = request.POST.get("description")
#             process_time = request.POST.get("process_time")
#             service_fees = request.POST.get("service_fees")

#             if service_name:
#                 # service_name=service_name.upper()
#                 found_data = Service.objects.filter(name=service_name)
#                 if found_data:
#                     messages.warning(request, "The service " +
#                                      service_name+", Already exist.")
#                     return redirect(services)
#                 else:
#                     # add new service
#                     add_service = Service(
#                         name=service_name,
#                         description=description,
#                         processingTime=process_time,
#                         fees=service_fees
#                     )
#                     add_service.save()

#                     messages.success(
#                         request, "New Service created successfully.")
#                     return redirect(services)
#             else:
#                 messages.error(request, "Error , Service name is required!")
#                 return redirect(services)
#         else:
#             request_data = Application.objects.filter(status="Waiting")
#             # getting services
#             ServiceData = Service.objects.filter()
#             context = {
#                 'title': 'Registrar - Service List',
#                 'service_active': 'active',
#                 'services': ServiceData,
#                 'request_data': request_data,
#             }
#             return render(request, 'main/dashboard/services.html', context)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)


# @login_required(login_url='manager_login')
# def servicesEdit(request, pk):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         service_id = pk
#         # getting service
#         if Service.objects.filter(id=service_id).exists():
#             # if exists
#             foundData = Service.objects.get(id=service_id)

#             if 'update_service' in request.POST:
#                 # Retrieve the form data from the request
#                 service_name = request.POST.get('service_name')
#                 description = request.POST.get('description')
#                 process_time = request.POST.get("process_time")
#                 fees = request.POST.get("service_fees")

#                 if service_name:
#                     if Service.objects.filter(name=service_name).exclude(id=service_id):
#                         messages.warning(
#                             request, "Service name already exist.")
#                         return redirect(servicesEdit, pk)
#                     else:
#                         # Update Service
#                         service_updated = Service.objects.filter(id=service_id).update(
#                             name=service_name,
#                             description=description,
#                             processingTime=process_time,
#                             fees=fees
#                         )
#                         if service_updated:
#                             messages.success(
#                                 request, "Service "+service_name+", Updated successfully.")
#                             return redirect(servicesEdit, pk)
#                         else:
#                             messages.error(request, ('Process Failed.'))
#                             return redirect(servicesEdit, pk)
#                 else:
#                     messages.error(request, ('Service name is required.'))
#                     return redirect(servicesEdit, pk)

#             elif 'delete_service' in request.POST:
#                 # Delete Service
#                 delete_service = Service.objects.get(id=service_id)
#                 delete_service.delete()
#                 messages.success(request, "Service info deleted successfully.")
#                 return redirect(services)

#             else:
#                 request_data = Application.objects.filter(status="Waiting")
#                 context = {
#                     'title': 'Registrar - Service Info',
#                     'service_active': 'active',
#                     'service': foundData,
#                     'request_data': request_data,
#                 }
#                 return render(request, 'main/dashboard/service_details.html', context)
#         else:
#             messages.error(request, ('Service not found'))
#             return redirect(services)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)


# @login_required(login_url='manager_login')
# def citizenList(request):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         if 'new_citizen' in request.POST:
#             first_name = request.POST.get("first_name")
#             last_name = request.POST.get("last_name")
#             nationality = request.POST.get("nationality")
#             nid_number = request.POST.get("nid_number")
#             birthdate = request.POST.get("birthdate")
#             birth_place = request.POST.get("birth_place")
#             gender = request.POST.get("gender")
#             marital_status = request.POST.get("marital_status")

#             if first_name and last_name and nationality and birthdate and birth_place and gender and marital_status:
#                 if Citizen.objects.filter(nid_number=nid_number).exists():
#                     messages.warning(request, "The citizen with " +
#                                      nid_number+", Already exist.")
#                     return redirect(citizenList)
#                 else:
#                     # add new citizen
#                     add_citizen = Citizen(
#                         first_name=first_name,
#                         last_name=last_name,
#                         nationality=nationality,
#                         nid_number=nid_number,
#                         birthdate=birthdate,
#                         birth_place=birth_place,
#                         gender=gender,
#                         marital_status=marital_status,
#                     )
#                     add_citizen.save()

#                     messages.success(
#                         request, "Citizen registered successfully.")
#                     return redirect(citizenList)
#             else:
#                 messages.error(request, ('All fields are required.'))
#                 return redirect(citizenList)
#         else:
#             request_data = Application.objects.filter(status="Waiting")
#             # getting citizens
#             CitizenData = Citizen.objects.filter()
#             context = {
#                 'title': 'Registrar - Citizen List',
#                 'citizenList_active': 'active',
#                 'citizens': CitizenData,
#                 'request_data': request_data,
#             }
#             return render(request, 'main/dashboard/citizen_list.html', context)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)


# @login_required(login_url='manager_login')
# def citizenEdit(request, pk):
#     if request.user.is_authenticated and request.user.is_manager == True:
#         citizen_id = pk
#         # getting citizen
#         if Citizen.objects.filter(id=citizen_id).exists():
#             # if exists
#             citizenData = Citizen.objects.get(id=citizen_id)
#             # get parent data
#             parentData = CitizenParent.objects.filter(citizen=citizen_id)
#             # get document data
#             documentData = CitizenDocument.objects.filter(citizen=citizen_id)

#             if 'update_citizen' in request.POST:
#                 # Retrieve the form data from the request
#                 first_name = request.POST.get("first_name")
#                 last_name = request.POST.get("last_name")
#                 nationality = request.POST.get("nationality")
#                 nid_number = request.POST.get("nid_number")
#                 birthdate = request.POST.get("birthdate")
#                 birth_place = request.POST.get("birth_place")
#                 gender = request.POST.get("gender")
#                 marital_status = request.POST.get("marital_status")

#                 if first_name and last_name and nationality and birthdate and birth_place and gender and marital_status:

#                     if Citizen.objects.filter(nid_number=nid_number).exclude(id=citizen_id).exists():
#                         messages.warning(request, "The citizen with " +
#                                          nid_number+", Already exist.")
#                         return redirect(citizenEdit, pk)
#                     else:
#                         # Update Service
#                         citizen_updated = Citizen.objects.filter(id=citizen_id).update(
#                             first_name=first_name,
#                             last_name=last_name,
#                             nationality=nationality,
#                             nid_number=nid_number,
#                             birthdate=birthdate,
#                             birth_place=birth_place,
#                             gender=gender,
#                             marital_status=marital_status,
#                         )
#                         if citizen_updated:
#                             messages.success(
#                                 request, "Citizen profile updated successfully.")
#                             return redirect(citizenEdit, pk)
#                         else:
#                             messages.error(request, ('Process Failed.'))
#                             return redirect(citizenEdit, pk)
#                 else:
#                     messages.error(request, ('All fields are required.'))
#                     return redirect(citizenEdit, pk)

#             elif 'update_address' in request.POST:
#                 # Retrieve the form data from the request
#                 region = request.POST.get("region")
#                 cercle = request.POST.get("cercle")
#                 commune = request.POST.get("commune")
#                 village = request.POST.get("village")

#                 if region and cercle and commune and village:
#                     # Update address
#                     address_updated = CitizenAddress.objects.filter(citizen=citizen_id).update(
#                         region=region,
#                         cercle=cercle,
#                         commune=commune,
#                         village=village
#                     )
#                     if address_updated:
#                         messages.success(
#                             request, "Citizen address updated successfully.")
#                         return redirect(citizenEdit, pk)
#                     else:
#                         messages.error(request, ('Process Failed.'))
#                         return redirect(citizenEdit, pk)
#                 else:
#                     messages.error(request, ('All fields are required.'))
#                     return redirect(citizenEdit, pk)

#             elif 'update_parents' in request.POST:
#                 father_fname = request.POST.get("father_fname")
#                 father_lname = request.POST.get("father_lname")
#                 father_profession = request.POST.get("father_profession")
#                 mother_fname = request.POST.get("mother_fname")
#                 mother_lname = request.POST.get("mother_lname")
#                 mother_profession = request.POST.get("mother_profession")

#                 if father_fname and father_lname and father_profession and mother_fname and mother_lname and mother_profession:
#                     # Update address
#                     parentF_updated = CitizenParent.objects.filter(citizen=citizen_id, parent="Father").update(
#                         first_name=father_fname,
#                         last_name=father_lname,
#                         professionalism=father_profession
#                     )
#                     parentM_updated = CitizenParent.objects.filter(citizen=citizen_id, parent="Mother").update(
#                         first_name=mother_fname,
#                         last_name=mother_lname,
#                         professionalism=mother_profession
#                     )
#                     if parentF_updated and parentM_updated:
#                         messages.success(
#                             request, "Citizen parent info updated successfully.")
#                         return redirect(citizenEdit, pk)
#                     else:
#                         messages.error(request, ('Process Failed.'))
#                         return redirect(citizenEdit, pk)
#                 else:
#                     messages.error(request, ('All fields are required.'))
#                     return redirect(citizenEdit, pk)

#             elif 'delete' in request.POST:
#                 # Delete Citizen
#                 delete_citizen = Citizen.objects.get(id=citizen_id)
#                 delete_citizen.delete()
#                 messages.success(request, "Citizen info deleted successfully.")
#                 return redirect(citizenList)

#             else:
#                 request_data = Application.objects.filter(status="Waiting")
#                 context = {
#                     'title': 'Registrar - Citizen Info',
#                     'citizenList_active': 'active',
#                     'citizen': citizenData,
#                     'parents': parentData,
#                     'documents': documentData,
#                     'request_data': request_data,
#                 }
#                 return render(request, 'main/dashboard/citizen_info.html', context)
#         else:
#             messages.error(request, ('Citizen not found'))
#             return redirect(citizenList)
#     else:
#         messages.warning(request, ('You have to login to view the page!'))
#         return redirect(managerLogin)

    