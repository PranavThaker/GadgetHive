from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    session_key = models.CharField(max_length = 60,null = True,blank=True)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added_at"]

    def __str__(self):
        owner = self.user.username if self.user else self.session_key
        return owner + " -> " + self.product.name + " x " + str(self.quantity)
    
    def subtotal(self):
        return self.product.price*self.quantity