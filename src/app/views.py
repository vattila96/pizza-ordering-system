import datetime
import base64
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import gettext as _
from .models import *
from .domain.models import *
from django import forms
from django.views.decorators.http import require_POST
from .cart import Cart


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(FoodProduct, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    print(cart)
    for item in cart:
      print(item)
    return render(request, 'shoppingcart.html', {'cart': cart})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = FoodProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(FoodProduct, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/product/detail.html', context)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def index(request):
    p = Post(date=datetime.datetime.now(), photo=random_picture())
    p.save(force_insert=True)
    posts = Post.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts': posts, "home_page": "active"})


def pizzas(request):
    Pizza(name="Brutalis", description="Betegmódon csípős pizza, fullba vedd meg!").save()
    Pizza(name="Extra finom", description="Nagyon finom pizza, belekóstolsz, vége. Még a tányért is...").save()
    Pizza(name="SAMPLE TEXT", description="SAMPLE PIZZA").save()
    pizzas = Pizza.objects.all().order_by('-name')

    test_translate = _("(teszt fordítás)")
    return render(request, 'pizza/pizzexample.html', {'pizzas': pizzas,
                                                      'test': test_translate, })


def random_picture():
    url = "https://source.unsplash.com/random/400x400"
    response = requests.get(url, stream=True)
    encoded_string = base64.b64encode(response.content)
    del response
    return encoded_string.decode('ascii')


def profile(request):
    context = {"profile_page": "active"}
    return render(request, 'profile.html', context)


def pizzalist(request):
    if request.method == 'POST':
        keyword = request.POST.get("custompizza_name", None)
        pizza_price = request.POST.get("custompizza_price", None)
        Pizza(name=keyword, description="Custom pizza", is_custom_pizza=True, price=pizza_price).save()

    pizzas = Pizza.objects.all().order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas}
    return render(request, 'pizzalist.html', context)


def pizzasearch(request):
    keyword = request.POST.get("search_keyword", None)
    name_contains = Pizza.objects.filter(name__icontains=keyword)
    description_contains = Pizza.objects.filter(description__icontains=keyword)
    pizzas = (name_contains | description_contains).order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas}
    return render(request, 'pizzalist.html', context)

def myorders(request):
    myorders = []

    for order in Order.objects.filter(O_T_M_User_Orders = request.user):
      sum = 0
      actorderitems = []
      for orderitem in OrderItem.objects.filter(O_T_M_Order_OrderItems = order):
        for food in FoodProduct.objects.filter(orderitems = orderitem):
          actorderitems.append(food)
          sum += food.price
        for drink in DrinkProduct.objects.filter(orderitems = orderitem):
          actorderitems.append(drink)
          sum += drink.price

      try:
        myorders.append((actorderitems, sum, order.transaction.currency, order))
      except Exception:
        myorders.append((actorderitems, sum, "HUF", order))

      myorders = myorders[-3:]

    context = {"myorders_page": "active",
               "myorders": myorders}
    return render(request, 'myorders.html', context)
