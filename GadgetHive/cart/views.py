from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from store.models import Product
from .models import CartItem


# Create your views here.

def _get_owner(request):
    if request.user.is_authenticated:
        return {"user":request.user,"session_key":None}
    if not request.session.session_key:
        request.session.create()
    return {"user":None,"session_key":request.session.session_key}

def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id,is_active=True)
    owner = _get_owner(request)
    item,_ = CartItem.objects.get_or_create(product=product,**owner)
    if _:
        item.quantity = 1
    else:
        item.quantity += 1
    item.save()
    return redirect("cart:detail")

def remove_from_cart(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    item.delete()
    return redirect("cart:detail")

def clear_cart(request):
    owner = _get_owner(request)
    CartItem.objects.filter(**owner).delete()
    return redirect ("cart:detail")

def cart_detail(request):
    owner = _get_owner(request)
    items = CartItem.objects.filter(**owner).select_related("product")
    total = sum(i.subtotal() for i in items)
    return render(request, "cart/detail.html",{"items":items,"total":total})