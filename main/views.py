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
        context = {
            'title': 'Welcome',
            'categories': categories,
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
        products = Product.objects.filter(product__category=selectedCategory)

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
        quantity = float(request.POST.get('qty'))
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
                cart_item['quantity'] = float(quantity)
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