from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("category/<slug:slug>/",views.category,name="category"),
    path("product/<slug:slug>/",views.product_detail,name="product"),
    path("search/",views.search,name="search"),
]