from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display=[]
# Register your models here.

admin.site.register(models.Customer)
# admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)

@admin.register(models.Product)
class ProducAdmin(admin.ModelAdmin):
    list_display=['name', 'description', 'price', 'in_stock']

    def price(self,obj):
        return '$. {:,}'.format(obj.unit_price)