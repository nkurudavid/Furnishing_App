import random
from django.utils import timezone
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
        matched_products = Product.objects.filter(
            Q(category__category_name__icontains=search_data) | Q(product_name__icontains=search_data))
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
        return render(request, '404.html', context)


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
            'home_active': 'active',
            'categories': categories,
            'products': selected_products,
        }
        return render(request, 'home.html', context)


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
            'about_active': 'active',
        }
        return render(request, 'about.html', context)


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
            'contact_active': 'active',
        }
        return render(request, 'contact.html', context)


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
            'shop_active': 'active',
            'categories': categories,
            'products': products,
        }
        return render(request, 'shop.html', context)


def customOrder(request):
    if 'search' in request.POST:
        search_data = request.POST.get("search_data")

        if search_data:
            # Call the search_result function and pass the data
            return search_result(request, search_data)
        else:
            return redirect(shop)
    else:
        materials = Material.objects.filter()
        context = {
            'title': 'Shop - Custom order',
            'custom_active': 'active',
            'materials': materials,
        }
        return render(request, 'custom_order_material.html', context)


def customOrderForm(request, pk):
    material_id = pk
    # check if material exist
    if Material.objects.filter(id=material_id).exists():
        # if exists
        selectedMaterial = Material.objects.get(id=material_id)

        if 'search' in request.POST:
            search_data = request.POST.get("search_data")

            if search_data:
                # Call the search_result function and pass the data
                return search_result(request, search_data)
            else:
                return redirect(shop)
        elif 'new_order' in request.POST:
            design = request.FILES["design"]
            quantity = request.POST.get("quantity")
            description = request.POST.get("description")
            if design and quantity and description:
                if request.user.is_authenticated and request.user.is_client == True:
                    # Generate a random number for order number
                    order_no = random.randint(1, 100000)
                    # submit custom order
                    CustomOrder.objects.create(
                        client=request.user,
                        order_number=order_no,
                        material=selectedMaterial,
                        description=description,
                        quantity=quantity,
                        picture=design,
                    )
                    messages.success(
                        request, ('Your order is on waiting list!'))
                    return redirect(client_order_list)
                else:
                    messages.warning(
                        request, ('You have to login to view the page!'))
                    return redirect(customOrderForm, pk)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(customOrderForm, pk)
        else:
            context = {
                'title': 'Shop - Custom order',
                'custom_active': 'active',
                'material': selectedMaterial,
            }
            return render(request, 'custom_order_form.html', context)
    else:
        messages.error(request, ('Material not found'))
        return redirect(customOrder)


def search_result(request, search_data=None):
    if search_data:
        # Call the search_products_filter function to get the filtered products
        filtered_products = search_products_filter(search_data)

        categoryData = ProductCategory.objects.filter()
        context = {
            'title': 'Shop - Search Result',
            'shop_active': 'active',
            'categories': categoryData,
            'products': filtered_products,
        }
        return render(request, 'search_result.html', context)
    else:
        return redirect(shop)


def shopCategory(request, name):
    category_name = name
    # check if category exist
    if ProductCategory.objects.filter(category_name=category_name).exists():
        # if exists
        selectedCategory = ProductCategory.objects.get(
            category_name=category_name)
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
                'shop_active': 'active',
                'categories': categories,
                'products': products,
                'selectedCategory': selectedCategory,
            }
            return render(request, 'shop.html', context)
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
                'shop_active': 'active',
                'categories': categories,
                'p_data': selected_product,
            }
            return render(request, 'product_details.html', context)
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
            context = {
                'title': 'Shop - Cart',
                'shop_active': 'active',
                'cart_items': cart_items,
                'total_price': total_price,
            }
            return render(request, 'shop_cart.html', context)


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
    if request.user.is_authenticated and request.user.is_client == True:
        if 'search' in request.POST:
            search_data = request.POST.get("search_data")
            if search_data:
                # Call the search_result function and pass the data
                return search_result(request, search_data)
            else:
                return redirect(shop)
        else:
            return render(request, 'checkout.html')
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)


@login_required(login_url='shop')
def order_confirmation(request):
    if request.user.is_authenticated and request.user.is_client == True:
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
                client=request.user,
                order_number=order_no,
                status='Pending',
                shipping_address=shipping_location+"/ "+shipping_street,
                total_amount=total_price,
                payment_method=pay_method,
                payment_id=payment_id,
            )
            client_order.save()
            if client_order:
                for product_id, item in cart.items():
                    details = OrderDetail(
                        order=client_order,
                        product=Product.objects.get(id=int(product_id)),
                        quantity=item['quantity'],
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
    if not request.user.is_authenticated or request.user.is_client != True:
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_client == True:
                login(request, user)
                messages.success(
                    request, ('Hi '+user.first_name+', you are logged in'))
                return redirect(client_dashboard)
            else:
                messages.error(
                    request, ('User Email or Password is not correct! Try agin...'))
                return redirect(shop)
    else:
        return redirect(client_dashboard)


def client_register(request):
    if not request.user.is_authenticated or request.user.is_client != True:
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
                        client_profile, created = ClientProfile.objects.get_or_create(
                            client=client)

                        # update client profile and save
                        client_profile.phone_number = phone_number
                        client_profile.location = location
                        client_profile.save()

                    user = authenticate(
                        request, email=email, password=password1)
                    if user is not None and user.is_client == True:
                        login(request, user)
                        messages.success(
                            request, ('Hi '+user.first_name+', you are logged in'))
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
    if request.user.is_authenticated and request.user.is_client == True:
        # client orders
        orders = Order.objects.filter(client=request.user)

        customOrders_data = CustomOrder.objects.filter(client=request.user).exclude(
            Q(status="Completed") | Q(status="Cancelled"))

        new_orders = Order.objects.filter(
            client=request.user).exclude(status='Success').count() + customOrders_data.count()
        context = {
            'title': 'Client Account',
            'account_active': 'active',
            'orders': orders,
            'new_orders': new_orders,
            'dashboard_active': 'active',
        }
        return render(request, 'client_account.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)


@login_required(login_url='shop')
def client_order_list(request):
    if request.user.is_authenticated and request.user.is_client == True:
        # client orders
        orders = Order.objects.filter(
            client=request.user).order_by('-created_date', 'status')

        customOrders = CustomOrder.objects.filter(
            client=request.user).order_by('-created_date', 'status')
        context = {
            'title': 'Client Account',
            'account_active': 'active',
            'orders': orders,
            'customOrders': customOrders,
            'orders_active': 'active',
        }
        return render(request, 'client_order_list.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)


@login_required(login_url='shop')
def client_order_details(request, pk):
    if request.user.is_authenticated and request.user.is_client == True:
        order_id = pk
        if Order.objects.filter(client=request.user, pk=order_id).exists():
            # client orders
            order = Order.objects.get(client=request.user, pk=order_id)
            new_orders = Order.objects.filter(
                client=request.user).exclude(status='Success').count()
            context = {
                'title': 'Client Account',
                'account_active': 'active',
                'order': order,
                'new_orders': new_orders,
                'orders_active': 'active',
            }
            return render(request, 'client_order_details.html', context)
        else:
            messages.warning(request, ('Order not found'))
            return redirect(client_order_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)


@login_required(login_url='shop')
def client_customOrder_details(request, pk):
    if request.user.is_authenticated and request.user.is_client == True:
        customOrder_id = pk
        if CustomOrder.objects.filter(client=request.user, pk=customOrder_id).exists():
            # client orders
            customOrder = CustomOrder.objects.get(
                client=request.user, pk=customOrder_id)

            if 'client_reaction' in request.POST:
                # Retrieve the form data from the request
                reaction = request.POST.get("reaction")

                if reaction:
                    # Assuming there is only one Pro_forma related to the CustomOrder
                    pro_forma = customOrder.feedbacks
                    pro_forma.client_reaction = reaction
                    pro_forma.save()
                    messages.success(
                        request, "Reaction submitted successfully")
                    return redirect(client_customOrder_details, pk)
                else:
                    messages.error(
                        request, "Your react is required.")
                    return redirect(client_customOrder_details, pk)
            else:
                context = {
                    'title': 'Client Account',
                    'account_active': 'active',
                    'customOrder': customOrder,
                    'orders_active': 'active',
                }
                return render(request, 'client_customOrder_details.html', context)
        else:
            messages.warning(request, ('Order not found'))
            return redirect(client_order_list)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)


@login_required(login_url='shop')
def customOrderPayment(request):
    if request.user.is_authenticated and request.user.is_client == True:
        if 'order_payment' in request.POST:
            pay_method = request.POST.get("pay_method")
            payment_id = request.POST.get("payment_id")
            proforma_id = request.POST.get("proforma_id")

            # add new order
            # get proforma with id = proforma_id
            customOrderPayment = Pro_forma.objects.get(id=proforma_id)

            customOrderPayment.payment_method = pay_method
            customOrderPayment.payment_id = payment_id
            customOrderPayment.payment_date = timezone.now()
            customOrderPayment.save()

            messages.success(request, ('Payment success!'))
            return redirect(client_order_list)
        else:
            messages.success(request, ('Oops! error in placing order.'))
            return redirect(shop_checkout)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop_checkout)


@login_required(login_url='shop')
def client_profile(request):
    if request.user.is_authenticated and request.user.is_client == True:
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
                c_profile, created = ClientProfile.objects.get_or_create(
                    client=get_user_model().objects.get(email=request.user.email))

                # update client profile and save
                c_profile.phone_number = phone_number
                c_profile.location = location
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
                c_profile, created = ClientProfile.objects.get_or_create(
                    client=get_user_model().objects.get(email=request.user.email))

                # update client shipping address and save
                c_profile.shipping_location = shipping_location
                c_profile.shipping_street = shipping_street
                c_profile.save()

                messages.success(
                    request, ('Shipping address updated successfully'))
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
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(client_profile)
                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(client_profile)
                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(client_profile)
                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(client_profile)
            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(client_profile)
        else:
            new_orders = Order.objects.filter(
                client=request.user).exclude(status='Success').count()
            context = {
                'title': 'Client Profile',
                'account_active': 'active',
                'new_orders': new_orders,
                'profile_active': 'active',
            }
            return render(request, 'client_profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(shop)

#     # staff


def staffLogin(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        return redirect(manager_dashboard)
    elif request.user.is_authenticated and request.user.is_craftsman == True:
        return redirect(craftsman_dashboard)
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_manager == True:
                login(request, user)
                messages.success(
                    request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(manager_dashboard)
            elif user is not None and user.is_craftsman == True:
                login(request, user)
                messages.success(
                    request, ('Hi '+user.first_name+', Welcome back to the dashboard!'))
                return redirect(craftsman_dashboard)
            else:
                messages.error(
                    request, ('User Email or Password is not correct! Try agin...'))
                return redirect(staffLogin)
        else:
            context = {'title': 'Staff Login', }
            return render(request, 'staff/login.html', context)


@login_required(login_url='staff_login')
def staffLogout(request):
    logout(request)
    messages.info(request, ('You are now Logged out.'))
    return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_dashboard(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        clients = ClientProfile.objects.filter()
        craftsmen = get_user_model().objects.filter(is_craftsman=True)
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'Manager Dashboard',
            'dash_active': 'active',
            'orders_count': orders_data.count(),
            'customOrders_count': customOrders_data.count(),
            'orders_data': orders_data[:5],
            'customOrders_data': customOrders_data[:5],
            'clients_count': clients.count(),
            'craftsmen_count': craftsmen.count(),
            'clients': clients[:5],
            'craftsmen': craftsmen[:5],
        }
        return render(request, 'staff/manager/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
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
            new_orders = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            new_customOrders = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')
            context = {
                'title': 'Manager Profile',
                'new_orders': new_orders,
                'new_customOrders': new_customOrders,
            }
            return render(request, 'staff/manager/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_craftsmanList(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_craftsman' in request.POST:
            # Retrieve the form data from the request
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')

            if first_name and last_name and email and gender:
                if get_user_model().objects.filter(email=email):
                    messages.warning(request, "Email already exist.")
                    return redirect(manager_craftsmanList)
                else:
                    # Create new User as chief_commune
                    user = get_user_model().objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password='user12345',
                        gender=gender,
                        is_craftsman=True,
                    )
                    if user:
                        messages.success(
                            request, "Craftsman: "+first_name+" "+last_name+", added successfully.")
                        return redirect(manager_craftsmanList)
                    else:
                        messages.error(request, ('Process Failed.'))
                        return redirect(manager_craftsmanList)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(manager_craftsmanList)
        else:
            # getting data
            craftsmen = get_user_model().objects.filter(is_craftsman=True)
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            context = {
                'title': 'Craftsman List',
                'craftsman_active': 'active',
                'craftsmen': craftsmen,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/craftsmenList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_craftsmanDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        member_id = pk
        # getting
        if get_user_model().objects.filter(is_craftsman=True, id=member_id).exists():
            # if exists
            foundData = get_user_model().objects.get(id=member_id)

            if 'update_craftsman' in request.POST:
                # Retrieve the form data from the request
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                gender = request.POST.get('gender')
                # profilePicture = request.FILES.get('profilePicture')

                if first_name and last_name and email and gender:
                    if get_user_model().objects.filter(email=email).exclude(id=member_id):
                        messages.warning(request, "Email already exist.")
                        return redirect(manager_craftsmanDetails, pk)
                    else:
                        # Update craftsman data
                        foundData.first_name = first_name
                        foundData.last_name = last_name
                        foundData.email = email
                        foundData.gender = gender
                        foundData.save()

                        messages.success(
                            request, "Craftsman: "+first_name+" "+last_name+", Updated successfully.")
                        return redirect(manager_craftsmanDetails, pk)
                else:
                    messages.error(
                        request, ('Error , All fields are required!'))
                    return redirect(manager_craftsmanDetails, pk)

            elif 'delete_craftsman' in request.POST:
                # Delete craftsman
                foundData.delete()
                messages.success(
                    request, "Craftsman info deleted successfully.")
                return redirect(manager_craftsmanList)

            else:
                # getting data
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                context = {
                    'title': 'Craftsman Info',
                    'craftsman_active': 'active',
                    'craftsman': foundData,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/manager/craftsmanDetails.html', context)
        else:
            messages.error(request, ('Craftsman info not found'))
            return redirect(manager_craftsmanList)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_productCategory(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_pCategory' in request.POST:
            category_name = request.POST.get("category_name")

            if category_name:
                found_data = ProductCategory.objects.filter(
                    category_name=category_name)
                if found_data:
                    messages.warning(
                        request, "The product category "+category_name+", Already exist.")
                    return redirect(manager_productCategory)
                else:
                    # add new product category
                    addCategory = ProductCategory(
                        category_name=category_name,
                    )
                    addCategory.save()

                    messages.success(
                        request, "New Product category created successfully.")
                    return redirect(manager_productCategory)
            else:
                messages.error(request, "Error , Category name is required!")
                return redirect(manager_productCategory)
        else:
            # getting data
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            categoryData = ProductCategory.objects.filter().order_by('category_name')
            context = {
                'title': 'Product category List',
                'product_active': 'active',
                'categoryActive': 'active',
                'categories': categoryData,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/productCategoryList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
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
                            messages.success(
                                request, "Category "+category_name+", Updated successfully.")
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
                messages.success(
                    request, "Product category info deleted successfully.")
                return redirect(manager_productCategory)

            else:
                # getting data
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                context = {
                    'title': 'ProductCategory Info',
                    'product_active': 'active',
                    'categoryActive': 'active',
                    'category': foundData,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/manager/productCategoryDetails.html', context)
        else:
            messages.error(request, ('Product category not found'))
            return redirect(manager_productCategory)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_product(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_product' in request.POST:
            category_id = request.POST.get("category")
            product_name = request.POST.get("product_name")
            description = request.POST.get("description")
            color = request.POST.get("color")
            price = request.POST.get("price")
            quantity = request.POST.get("quantity")
            product_image1 = request.FILES["product_image1"]
            product_image2 = request.FILES["product_image2"]

            if category_id and product_name and price and color and quantity and product_image1 and product_image2:
                # check if existing product
                if Product.objects.filter(category=category_id, product_name=product_name).exists():
                    messages.warning(request, "The product name " +
                                     product_name+", Already exist.")
                    return redirect(manager_product)
                else:
                    # add new product
                    newProduct = Product.objects.create(
                        category=ProductCategory.objects.get(pk=category_id),
                        product_name=product_name,
                        description=description,
                        color=color,
                        price=float(price),
                        quantity=int(quantity),
                    )
                    # Create ProductImage instances and associate them with the product
                    ProductImage.objects.create(
                        product=newProduct, picture=product_image1)
                    ProductImage.objects.create(
                        product=newProduct, picture=product_image2)

                    messages.success(
                        request, "New product created successfully.")
                    return redirect(manager_product)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(manager_product)
        else:
            # getting data
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            categoriesData = ProductCategory.objects.filter().order_by('category_name')
            # getting communes
            productsData = Product.objects.filter().order_by('category', 'product_name')
            context = {
                'title': 'Management - Products List',
                'product_active': 'active',
                'productActive': 'active',
                'categories': categoriesData,
                'products': productsData,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/productList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_productDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        product_id = pk
        # getting product
        if Product.objects.filter(id=product_id).exists():
            # if exists
            foundData = Product.objects.get(id=product_id)

            if 'update_productInfo' in request.POST:
                # Retrieve the form data from the request
                category_id = request.POST.get("category")
                product_name = request.POST.get("product_name")
                description = request.POST.get("description")
                color = request.POST.get("color")
                price = request.POST.get("price")
                quantity = request.POST.get("quantity")

                if category_id and product_name and description and price and color and quantity:
                    if Product.objects.filter(category=category_id, product_name=product_name).exclude(id=product_id).exists():
                        messages.warning(
                            request, "Product name already exist.")
                        return redirect(manager_productDetails, pk)
                    else:
                        # Update product
                        foundData.category = ProductCategory.objects.get(
                            id=category_id)
                        foundData.product_name = product_name
                        foundData.description = description
                        foundData.price = float(price)
                        foundData.color = color
                        foundData.quantity = int(quantity)
                        foundData.save()

                        messages.success(request, "Product " +
                                         product_name+", Updated successfully.")
                        return redirect(manager_productDetails, pk)
                else:
                    messages.error(
                        request, ('Error!, All fields are required.'))
                    return redirect(manager_productDetails, pk)

            elif 'delete_product' in request.POST:
                # Delete product
                foundData.delete()
                messages.success(request, "Product info deleted successfully.")
                return redirect(manager_product)

            else:
                # getting data
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                # getting Product categories
                categoriesData = ProductCategory.objects.filter().order_by('category_name')
                context = {
                    'title': 'Management - Product Info',
                    'product_active': 'active',
                    'productActive': 'active',
                    'categories': categoriesData,
                    'product': foundData,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/manager/productDetails.html', context)
        else:
            messages.error(request, ('Product not found'))
            return redirect(manager_product)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_materials(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        if 'new_material' in request.POST:
            material_name = request.POST.get("material_name")
            description = request.POST.get("description")
            material_image = request.FILES["material_image"]

            if material_name and description and material_image:
                # check if existing material
                if Material.objects.filter(name=material_name).exists():
                    messages.warning(request, "The material name " +
                                     material_name+", Already exist.")
                    return redirect(manager_materials)
                else:
                    # add new material
                    Material.objects.create(
                        name=material_name,
                        description=description,
                        picture=material_image,
                    )

                    messages.success(
                        request, "New material recorded successfully.")
                    return redirect(manager_materials)
            else:
                messages.error(request, "Error , All fields are required!")
                return redirect(manager_materials)
        else:
            # getting data
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            materialsData = Material.objects.filter().order_by('name')
            context = {
                'title': 'Materials List',
                'materialActive': 'active',
                'materialsData': materialsData,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/materialsList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_materialDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        material_id = pk
        # getting Material
        if Material.objects.filter(id=material_id).exists():
            # if exists
            foundData = Material.objects.get(id=material_id)

            if 'update_materialInfo' in request.POST:
                # Retrieve the form data from the request
                material_name = request.POST.get("material_name")
                description = request.POST.get("description")

                if material_name and description:
                    if Material.objects.filter(name=material_name).exclude(id=material_id).exists():
                        messages.warning(
                            request, "Material name already exist.")
                        return redirect(manager_materialDetails, pk)
                    else:
                        # Update material
                        foundData.name = material_name
                        foundData.description = description
                        foundData.save()

                        messages.success(request, "Material " +
                                         material_name+", Updated successfully.")
                        return redirect(manager_materialDetails, pk)
                else:
                    messages.error(
                        request, ('Error!, All fields are required.'))
                    return redirect(manager_materialDetails, pk)

            if 'update_materialImage' in request.POST:
                # Retrieve the form data from the request
                material_image = request.FILES["material_image"]

                if material_image:
                    # Update material image
                    foundData.picture = material_image
                    foundData.save()

                    messages.success(
                        request, "Material Image Updated successfully.")
                    return redirect(manager_materialDetails, pk)
                else:
                    messages.error(
                        request, ('Image is required.'))
                    return redirect(manager_materialDetails, pk)

            elif 'delete_material' in request.POST:
                # Delete product
                foundData.delete()
                messages.success(
                    request, "Material info deleted successfully.")
                return redirect(manager_materials)

            else:
                # getting data
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                context = {
                    'title': 'Material Details',
                    'materialActive': 'active',
                    'material': foundData,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/manager/materialDetails.html', context)
        else:
            messages.error(request, ('Material info not found'))
            return redirect(manager_materials)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_clientList(request):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        clientsData = ClientProfile.objects.filter().order_by('client__first_name')
        context = {
            'title': 'Management - Clients List',
            'client_active': 'active',
            'clients': clientsData,
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/clientsList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_clientDetails(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        client_id = pk
        # getting client profile
        if ClientProfile.objects.filter(id=client_id).exists():
            # if exists
            foundData = ClientProfile.objects.get(id=client_id)

            # getting data
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            context = {
                'title': 'Management - Client Info',
                'client_active': 'active',
                'data': foundData,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/clientDetails.html', context)
        else:
            messages.error(request, ('Client info not found'))
            return redirect(manager_clientList)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_newOrder(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'Management - New Orders',
            'order_active': 'open active',
            'newOrder_active': 'active',
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/newOrdersList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_newOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if Order.objects.filter(id=newOrder_id).exclude(status="Success").exists():
            clientOrder = Order.objects.get(id=newOrder_id)

            if 'take_action' in request.POST:
                # Retrieve the form data from the request
                action_status = request.POST.get("action_status")

                if action_status:
                    # update the status
                    clientOrder.status = action_status
                    clientOrder.save()

                    messages.success(
                        request, "Action on Client Order applied successfully")
                    return redirect(manager_newOrderDetails, pk)
                else:
                    messages.error(
                        request, "Make sure to select action on this order.")
                    return redirect(manager_newOrderDetails, pk)
            else:
                # getting data
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                context = {
                    'title': 'Management - New order details',
                    'order_active': 'open active',
                    'newOrder_active': 'active',
                    'clientOrder': clientOrder,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/manager/newOrderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(manager_newOrder)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_archieviedOrder(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        # getting archieved orders
        completedOrders = Order.objects.filter(
            status="Success").order_by('created_date')
        context = {
            'title': 'Management - Archieved Orders',
            'order_active': 'open active',
            'archievedOrder_active': 'active',
            'completedOrders': completedOrders,
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/archievedOrdersList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_archievedOrderDetails(request, pk):
    completedOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if Order.objects.filter(id=completedOrder_id, status="Success").exists():
            completedOrder = Order.objects.get(
                id=completedOrder_id, status="Success")

            # getting data
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            context = {
                'title': 'Management - Archieved order details',
                'order_active': 'open active',
                'archievedOrder_active': 'active',
                'clientOrder': completedOrder,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/archievedOrderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(manager_archieviedOrder)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_inventory(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting data
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        foundData = StockMovement.objects.filter().order_by('date_time')
        context = {
            'title': 'Management - Stock Inventory',
            'inventory_active': 'active',
            'inventories': foundData,
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/inventory.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_newCustomOrders(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        # getting new request
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'New Custom Orders',
            'customOrder_active': 'open active',
            'newCustomOrder': 'active',
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/customOrderList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_newCustomOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if CustomOrder.objects.filter(id=newOrder_id).exclude(Q(status="Completed") | Q(status="Cancelled")).exists():
            clientOrder = CustomOrder.objects.get(id=newOrder_id)

            if 'assignCraftsman' in request.POST:
                # Retrieve the form data from the request
                craftsman_id = request.POST.get("craftsman")

                if craftsman_id:
                    # update the processed_by
                    clientOrder.processed_by = get_user_model().objects.get(id=craftsman_id)
                    clientOrder.save()

                    messages.success(
                        request, "Craftsman assigned successfully")
                    return redirect(manager_newCustomOrderDetails, pk)
                else:
                    messages.error(
                        request, "Make sure to select craftsman.")
                    return redirect(manager_newCustomOrderDetails, pk)

            elif 'take_action' in request.POST:
                # Retrieve the form data from the request
                action_status = request.POST.get("action_status")

                if action_status:
                    # update the status
                    clientOrder.status = action_status
                    clientOrder.save()

                    messages.success(
                        request, "Action on Client Order applied successfully")
                    return redirect(manager_newCustomOrderDetails, pk)
                else:
                    messages.error(
                        request, "Make sure to select action on this order.")
                    return redirect(manager_newCustomOrderDetails, pk)
            else:
                # getting new request
                orders_data = Order.objects.filter().exclude(
                    status="Success").order_by('status', 'created_date')
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                craftsmen = get_user_model().objects.filter(is_craftsman=True)

                context = {
                    'title': 'New Custom Order details',
                    'customOrder_active': 'open active',
                    'newCustomOrder': 'active',
                    'clientOrder': clientOrder,
                    'orders_data': orders_data,
                    'customOrders_data': customOrders_data,
                    'craftsmen': craftsmen,
                }
                return render(request, 'staff/manager/customOrderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(manager_newCustomOrders)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_completedCustomOrders(request,):
    if request.user.is_authenticated and request.user.is_manager == True:
        completedOrders = CustomOrder.objects.filter(
            Q(status="Completed") | Q(status="Cancelled")).order_by('created_date')
        # getting new request
        orders_data = Order.objects.filter().exclude(
            status="Success").order_by('status', 'created_date')
        customOrders_data = CustomOrder.objects.filter().exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'Completed Custom Orders List',
            'customOrder_active': 'open active',
            'completedOrder': 'active',
            'completedOrders': completedOrders,
            'orders_data': orders_data,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/manager/archievedCustomOrderList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def manager_completedCustomOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_manager == True:
        if CustomOrder.objects.filter(Q(status="Completed") | Q(status="Cancelled")).filter(id=newOrder_id).exists():
            clientOrder = CustomOrder.objects.get(id=newOrder_id)

            # getting new request
            orders_data = Order.objects.filter().exclude(
                status="Success").order_by('status', 'created_date')
            customOrders_data = CustomOrder.objects.filter().exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            context = {
                'title': 'Completed Custom Order Details',
                'customOrder_active': 'open active',
                'completedOrder': 'active',
                'clientOrder': clientOrder,
                'orders_data': orders_data,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/manager/archievedCustomOrderDetails.html', context)
        else:
            messages.warning(request, ('Command not found'))
            return redirect(manager_completedCustomOrders)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


# craftsman views


@login_required(login_url='staff_login')
def craftsman_dashboard(request):
    if request.user.is_authenticated and request.user.is_craftsman == True:
        # getting data
        newCustomOrder = CustomOrder.objects.filter(
            status="Pending", processed_by=request.user).order_by('created_date')
        tasks_data = CustomOrder.objects.filter(
            status="Processing", processed_by=request.user).order_by('created_date')
        # getting new request
        customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'Craftsman - Dashboard',
            'dash_active': 'active',
            'customOrders_count': newCustomOrder.count(),
            'tasks_count': tasks_data.count(),
            'customOrders_data': customOrders_data[:5],
        }
        return render(request, 'staff/craftsman/dashboard.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_profile(request):
    if request.user.is_authenticated and request.user.is_craftsman == True:
        if 'update_password' in request.POST:
            old_password = request.POST.get("old_pass")
            new_password = request.POST.get("pass1")
            confirmed_new_password = request.POST.get("pass2")

            if old_password and new_password and confirmed_new_password:
                user = get_user_model().objects.get(email=request.user.email)

                if not user.check_password(old_password):
                    messages.error(
                        request, "Your old password is not correct!")
                    return redirect(craftsman_profile)

                else:
                    if len(new_password) < 5:
                        messages.warning(request, "Your password is too weak!")
                        return redirect(craftsman_profile)

                    elif new_password != confirmed_new_password:
                        messages.error(
                            request, "Your new password not match the confirm password !")
                        return redirect(craftsman_profile)

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(
                            request, "Your password has been changed successfully.!")
                        return redirect(craftsman_profile)

            else:
                messages.error(request, "Error , All fields are required !")
                return redirect(craftsman_profile)

        else:
            # getting data
            # getting new request
            customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')
            context = {
                'title': 'My Profile',
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/craftsman/profile.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_materials(request):
    if request.user.is_authenticated and request.user.is_craftsman == True:
        # getting data
        # getting new request
        customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')
        materialsData = Material.objects.filter().order_by('name')
        context = {
            'title': 'Materials List',
            'materialActive': 'active',
            'materialsData': materialsData,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/craftsman/materialsList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_customOrders(request,):
    if request.user.is_authenticated and request.user.is_craftsman == True:
        # getting new request
        customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'New Custom Orders',
            'customOrder_active': 'open active',
            'newCustomOrder': 'active',
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/craftsman/customOrderList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_customOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_craftsman == True:
        if CustomOrder.objects.filter(id=newOrder_id, processed_by=request.user).exclude(Q(status="Completed") | Q(status="Cancelled")).exists():
            clientOrder = CustomOrder.objects.get(id=newOrder_id)

            if 'pro_forma' in request.POST:
                # Retrieve the form data from the request
                proforma_status = request.POST.get("proforma_status")
                payment_amount = request.POST.get("payment_amount")
                processing_period = request.POST.get("processing_period")

                if proforma_status:
                    if proforma_status and payment_amount and processing_period:
                        if Pro_forma.objects.filter(custom_order=clientOrder).exists():
                            proforma = Pro_forma.objects.get(
                                custom_order=clientOrder)
                            proforma.status = proforma_status
                            proforma.payment_amount = payment_amount
                            proforma.processing_period = processing_period
                            proforma.save()
                        else:
                            proForma = Pro_forma.objects.create(
                                custom_order=clientOrder,
                                status=proforma_status,
                                payment_amount=payment_amount,
                                processing_period=processing_period,
                                processed_by=request.user,
                            )
                    else:
                        if Pro_forma.objects.filter(custom_order=clientOrder).exists():
                            proforma = Pro_forma.objects.get(
                                custom_order=clientOrder)
                            proforma.status = proforma_status
                            proforma.payment_amount = 0
                            proforma.processing_period = 0
                            proforma.client_reaction = "None"
                            proforma.save()
                        else:
                            proForma = Pro_forma.objects.create(
                                custom_order=clientOrder,
                                status=proforma_status,
                                processed_by=request.user,
                                client_reaction="None",
                            )

                    if not Pro_forma.objects.filter(custom_order=clientOrder).exists():
                        if proForma:
                            subject = "Pro-forma Information for Your Custom Order"
                            if proForma.status == "Doable":
                                message = f"Dear {clientOrder.client.get_full_name()},\n\n" \
                                    f"We are pleased to provide you with the proforma information for your custom order:\n\n" \
                                    f"Order Number: #{clientOrder.order_number}\n" \
                                    f"Status: {proForma.status}\n" \
                                    f"Payment Amount: {proForma.payment_amount}\n" \
                                    f"Processing Period (Days): {proForma.processing_period}\n\n" \
                                    "Thank you for choosing us for your custom order.\n\n" \
                                    "Furnishing Order System (Doable Order)"
                            else:
                                message = f"Dear {clientOrder.client.get_full_name()},\n\n" \
                                    f"We regret to inform you that your custom order is undoable at this time.\n\n" \
                                    f"Order Number: #{clientOrder.order_number}\n" \
                                    f"Status: {proForma.status}\n\n" \
                                    "Please feel free to contact us for further assistance.\n\n" \
                                    "Furnishing Order System (Undoable Order)"

                            # Send the email
                            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [
                                clientOrder.client.email])
                            email.send()

                            messages.success(
                                request, "Pro-Forma sent successfully")
                            return redirect(craftsman_customOrderDetails, pk)
                        else:
                            messages.error(
                                request, "Proccess failed!.")
                            return redirect(craftsman_customOrderDetails, pk)
                    else:
                        messages.success(request, "Proforma Updated!.")
                        return redirect(craftsman_customOrderDetails, pk)
                else:
                    messages.error(
                        request, "Make sure to respond to this order.")
                    return redirect(craftsman_customOrderDetails, pk)
            else:
                # getting new request
                customOrders_data = CustomOrder.objects.filter().exclude(
                    Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

                context = {
                    'title': 'New Custom Order details',
                    'customOrder_active': 'open active',
                    'newCustomOrder': 'active',
                    'clientOrder': clientOrder,
                    'customOrders_data': customOrders_data,
                }
                return render(request, 'staff/craftsman/customOrderDetails.html', context)
        else:
            messages.warning(request, ('Client order not found'))
            return redirect(craftsman_customOrders)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_completedCustomOrders(request,):
    if request.user.is_authenticated and request.user.is_craftsman == True:
        completedOrders = CustomOrder.objects.filter(processed_by=request.user).filter(
            Q(status="Completed") | Q(status="Cancelled")).order_by('created_date')
        # getting new request
        customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
            Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

        context = {
            'title': 'Completed Custom Orders List',
            'customOrder_active': 'open active',
            'completedOrder_active': 'active',
            'completedOrders': completedOrders,
            'customOrders_data': customOrders_data,
        }
        return render(request, 'staff/craftsman/archievedCustomOrderList.html', context)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)


@login_required(login_url='staff_login')
def craftsman_completedCustomOrderDetails(request, pk):
    newOrder_id = pk
    if request.user.is_authenticated and request.user.is_craftsman == True:
        if CustomOrder.objects.filter(Q(status="Completed") | Q(status="Cancelled")).filter(id=newOrder_id, processed_by=request.user).exists():
            clientOrder = CustomOrder.objects.get(id=newOrder_id)

            # getting new request
            customOrders_data = CustomOrder.objects.filter(processed_by=request.user).exclude(
                Q(status="Completed") | Q(status="Cancelled")).order_by('status', 'created_date')

            context = {
                'title': 'Completed Custom Order Details',
                'customOrder_active': 'open active',
                'completedOrder_active': 'active',
                'clientOrder': clientOrder,
                'customOrders_data': customOrders_data,
            }
            return render(request, 'staff/craftsman/archievedCustomOrderDetails.html', context)
        else:
            messages.warning(request, ('Command not found'))
            return redirect(craftsman_completedCustomOrders)
    else:
        messages.warning(request, ('You have to login to view the page!'))
        return redirect(staffLogin)
