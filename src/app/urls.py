from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('pizzak/', views.pizzas, name='pizzas'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('pizzas/', views.pizzas, name='pizzas'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.update_profile, name='profile'),
    path('pizzalist/', views.pizzalist, name='pizzalist'),
    path('myorders/', views.myorders, name='myorders'),
    path('pizzalist/pizzaSearch', views.pizzasearch, name='pizzasearch'),
    path('shoppingcart', views.cart_detail, name='shoppingcart'),
    path('get-paid/', views.get_paid, name='getpaid'),
    path('pizzalist/pizzaReset', views.pizzareset, name='pizzareset'),
    path('pizzalist/categoryFilter', views.categoryfilter, name='categoryfilter'),
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
