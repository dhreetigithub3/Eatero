from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import razorpay
from django.conf import settings
from .models import Customer, Restaurant, Item, Cart
from .forms import CustomerSignupForm

# Create your views here.
def say_hello(request):
    #return HttpResponse("Sy Hello, My app is working")
    return render(request, "index.html")

def open_signup(request):
    return render(request, "signup.html")

def open_signin(request):
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "signin.html", {"success": "Account created! Please sign in."})
        else:
            return render(request, "signup.html", {"form": form})
    return render(request, "signup.html", {"form": CustomerSignupForm()})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


    try:
        Customer.objects.get(username = username, password = password)
        if username == 'admin':
            return render(request, 'admin_home.html')
        else:
            # restaurantList = Restaurant.objects.all()
            # return render(request, 'customer_home.html', {"restaurantList" : restaurantList, "username" : username})
            return customer_home(request, username)
        
    except Customer.DoesNotExist:
        return render(request, 'fail.html')

def admin_home(request):
    return render(request, 'admin_home.html')

def open_add_restaurant(request):
    return render(request, 'add_restaurant.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
    return render(request, 'admin_home.html')

def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html', {"restaurantList" : restaurantList})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant" : restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()
    
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})

def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def open_add_item(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'admin_add_item.html', {"restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def open_edit_item(request, item_id, restaurant_id):
    item = Item.objects.get(id = item_id)
    return render(request, 'admin_edit_item.html', {"item" : item, "restaurant_id" : restaurant_id})

def edit_item(request, item_id, restaurant_id):
    item = Item.objects.get(id = item_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')

        item.name = name
        item.description = description
        item.price = price
        item.vegeterian = vegeterian
        item.picture = picture

        item.save()

    return open_update_menu(request, restaurant_id)


def delete_item_menu(request, item_id, restaurant_id):
    item = Item.objects.get(id = item_id)
    item.delete()
    return open_update_menu(request, restaurant_id)

def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'customer_menu.html', {"itemList" : itemList, "restaurant" : restaurant, "username":username})

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = Customer.objects.get(username = username)

    cart, created = Cart.objects.get_or_create(customer = customer)

    cart.items.add(item)

    # result = show_cart(request, username) # Direct call
    # return HttpResponse(result)
    return show_cart(request, username)

def show_cart(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html', {"itemList" : items, "total_price" : total_price, "username":username})

def delete_item_cart(request, item_id, username):
    item = Item.objects.get(id=item_id)
    customer = Customer.objects.get(username=username)

    cart = Cart.objects.get(customer=customer)

    cart.items.remove(item)

    return show_cart(request, username)

def customer_home(request, username):
    restaurantList = Restaurant.objects.all()
    return render(request, 'customer_home.html', {"restaurantList" : restaurantList, "username" : username})

def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'checkout.html', {
            'error': 'Your cart is empty!',
        })
    # return render(request, 'checkout.html', {"username" : username, "cart_items" : cart_items, "total_price" : total_price})

# Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # Avoid failing through system proxy env vars in local dev.
    client.session.trust_env = False


    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    try:
        order = client.order.create(data=order_data)
    except Exception:
        return render(request, 'checkout.html', {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            'error': 'Payment service is currently unreachable. Please check your internet/proxy settings and try again.',
        })


    # Pass the order details to the frontend
    return render(request, 'checkout.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount_paise': order_data['amount'],
    })

def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    payment_method = request.GET.get('method', 'Online')
    # Fetch cart items and total price before clearing the cart
    cart_items = list(cart.items.all()) if cart else []
    total_price = cart.total_price() if cart else 0


    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()


    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'payment_method': payment_method,
    })
