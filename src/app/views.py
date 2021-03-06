import base64
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.http import require_POST

from .cart import Cart
from .domain.models import *
from .forms import *

PRODUCT_QUANTITY_CHOICES = [(i / 2, str(i / 2)) for i in range(1, 40)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=float)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


@require_POST
def cart_add(request, product_id):
    try:
        quan = 0.5
    except MultiValueDictKeyError as er:
        quan = 1.0

    cart = Cart(request)
    product = get_object_or_404(Pizza, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    else:
        cart.add(product=product, quantity=quan)
    return redirect('shoppingcart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizza, id=product_id)
    cart.remove(product)
    return redirect('shoppingcart')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        # item['quantity'] = int(item['quantity'])
    return render(request, 'shoppingcart.html', {'cart': cart})


def get_paid(request):
    status = request.GET.get('status')
    if status == "success":
        cart = Cart(request)
        courier = Courier.objects.all().order_by('id').first()
        address = Address.objects.get(O_T_M_User_Adresses=request.user)
        order = Order(
            O_T_M_User_Orders=request.user, status="Fizetve!", discount=10,
            delivery_date=datetime.now(), expected_giving_to_courier_date=datetime.now(),
            given_to_courier_date=datetime.now(), expected_delivery_date=datetime.now(),
            Courier_Orders_id=courier.id, comment="Best order ever!", O_T_O_Address_Order_id=address.id
        )
        # todo: add order items in another issue when pizzas are fixed!
        order.save()
        cart.clear()

        return render(request, 'successful-payment.html')

    return render(request, 'unsuccessful-payment.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    home_page_detail = HomePageDetail.objects.last()
    return render(request, 'index.html', {'home_page_detail': home_page_detail, "home_page": "active"})


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
        if keyword != "" and PizzaCategory.objects.count() > 0:
          pizza_price = request.POST.get("custompizza_price", None)
          Pizza(name=keyword, description="Custom pizza", category = PizzaCategory.objects.last(), is_custom_pizza=True).save()	
		  
    pizzas = Pizza.objects.all().order_by('-name')
    pizza_categories = PizzaCategory.objects.all().order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas, 'categories': pizza_categories}
    return render(request, 'pizzalist.html', context)


def categoryfilter(request):
    category = request.POST.get("category", None)
    if category == "all":
        pizzas = Pizza.objects.all().order_by('-name')
    else:
        pizzas = Pizza.objects.filter(category__name=category)
    pizza_categories = PizzaCategory.objects.all().order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas, 'categories': pizza_categories}
    return render(request, 'pizzalist.html', context)


def pizzasearch(request):
    keyword = request.POST.get("search_keyword", None)

    allergen_list = request.POST.getlist("allergens")

    allergen_correct_pizzas = Pizza.objects.all().order_by('-name')

    # Todo change hard-coded allergens to a new Class in the DB
    if "milk" in allergen_list:
        allergen_correct_pizzas = allergen_correct_pizzas.filter(contains_milk=False)

    if "peanuts" in allergen_list:
        allergen_correct_pizzas = allergen_correct_pizzas.filter(contains_peanuts=False)

    if "gluten" in allergen_list:
        allergen_correct_pizzas = allergen_correct_pizzas.filter(contains_gluten=False)

    if "fish" in allergen_list:
        allergen_correct_pizzas = allergen_correct_pizzas.filter(contains_fish=False)

    if "wheat" in allergen_list:
        allergen_correct_pizzas = allergen_correct_pizzas.filter(contains_wheat=False)

    name_contains = allergen_correct_pizzas.filter(name__icontains=keyword)
    description_contains = allergen_correct_pizzas.filter(description__icontains=keyword)
    pizzas = (name_contains | description_contains).order_by('-name')
    pizza_categories = PizzaCategory.objects.all().order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas, 'categories': pizza_categories}
    return render(request, 'pizzalist.html', context)


def pizzareset(request):
    keyword = request.POST.get("reset_keyword", None)
    pizzas = Pizza.objects.all().order_by('-name')
    pizza_categories = PizzaCategory.objects.all().order_by('-name')
    context = {'pizzalist_page': 'active', 'pizzas': pizzas, 'categories': pizza_categories}
    return render(request, 'pizzalist.html', context)


def myorders(request):
    myorders = []

    for order in Order.objects.filter(O_T_M_User_Orders=request.user):
        sum = 0
        actorderitems = []
        for orderitem in OrderItem.objects.filter(O_T_M_Order_OrderItems=order):
            for food in FoodProduct.objects.filter(orderitems=orderitem):
                actorderitems.append(food)
                sum += food.price
            for drink in DrinkProduct.objects.filter(orderitems=orderitem):
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


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
