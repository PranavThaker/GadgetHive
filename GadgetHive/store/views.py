from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from django.db.models import Q

# Create your views here.

def home(request):
    products = Product.objects.filter(is_active=True)[:12]
    category = Category.objects.all()
    return render(request,"store/home.html",{"products":products,"categories":category})

def category(request,slug):
    cat = get_object_or_404(Category,slug = slug)
    products = cat.products.filter(is_active=True)
    return render(request, "store/category.html", {"category": cat, "products": products})

def product_detail(request,slug):
    product = get_object_or_404(Product,slug=slug,is_active=True)
    return render(request,"store/product_detail.html",{"product":product})

def search(request):
    q = request.GET.get("q", "").strip()
    products = []
    if q:
        products = (
            Product.objects.filter(is_active=True)
            .filter(Q(name__icontains=q) | Q(description__icontains=q))
        )
    return render(request, "store/search.html", {"query": q, "products": products})