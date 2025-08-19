from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Order,OrderItem
from cart.models import CartItem


# Create your views here.
@login_required
def checkout(request):
    owner = {"user":request.user,"session_key":None}
    items = CartItem.objects.filter(**owner).select_related("product")
    if request.method=="POST":
        order = Order.objects.create(user = request.user,status = "pending",total = 0)
        total = Decimal("0.00")
        for c1 in items:
            OrderItem.objects.create(
                order=order,product = c1.product,quantity = c1.quantity,price=c1.product.price
            )
            total +=c1.product.price*c1.quantity
        order.total = total
        order.save()
        items.delete()
        return redirect("orders:success", pk=order.pk)
    return render(request,"orders/checkout.html",{"items":items})


@login_required
def order_list(request):
    order = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"orders/list.html",{"orders":order})


@login_required
def order_detail(request,pk):
    order = get_object_or_404(Order,pk=pk,user = request.user)
    return render(request,"orders/detail.html",{"order":order})


@login_required
def order_success(request,pk):
    order = get_object_or_404(Order,pk=pk,user = request.user)
    return render(request,"orders/success.html",{"order":order})