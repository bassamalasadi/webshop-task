from django.contrib import admin
from .models import Item, OrderItem, Order, UserProfile


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile)
