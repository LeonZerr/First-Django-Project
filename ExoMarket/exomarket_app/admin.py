from django.contrib import admin
from .models import CustomUser,Item,Cart,CartItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)