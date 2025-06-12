from django.contrib import admin
from .models import ProductCategory,Product,Producer,Cart,CartItem

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Producer)
admin.site.register(Cart)
admin.site.register(CartItem)
