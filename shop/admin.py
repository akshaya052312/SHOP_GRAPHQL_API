from django.contrib import admin
from .models import Shop, ShopEmail, ShopPhone

# Register your models here.

admin.site.register(Shop)
admin.site.register(ShopEmail)
admin.site.register(ShopPhone)
