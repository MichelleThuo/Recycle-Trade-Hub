from django.contrib import admin
from .models import Products, Cart, Order, MpesaPayment, Review


class MpesaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(MpesaPayment,MpesaAdmin )
