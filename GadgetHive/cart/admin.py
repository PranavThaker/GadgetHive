from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key", "product", "quantity", "added_at")
    list_filter = ("user", "added_at")
    search_fields = ("product__name", "session_key", "user__username")