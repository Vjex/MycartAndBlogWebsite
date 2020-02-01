from django.contrib import admin

# Register your models here.
from .models import Product
from .models import ContactUs, Orders, OrderUpdate

admin.site.register(Product)
admin.site.register(ContactUs)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
