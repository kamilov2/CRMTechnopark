from django.contrib import admin
from .models import Client, DragAndDrop, Product, Sales, PayProduct, Expense

class PayProductAdmin(admin.ModelAdmin):
    list_display = ('id_payment', 'id', 'name', 'product', 'quantity', 'price', 'pay_date')
    list_filter = ('product', 'pay_date')
    search_fields = ('name', 'id_payment')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('product','id', 'quantity_sold', 'sale_date')
    list_filter = ('product', 'sale_date')
    search_fields = ('product__name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'price', 'quantity_on_hand', 'shtrix')
    search_fields = ('name', 'shtrix')

class DragAndDropAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'reg_date', 'special_key')
    filter_horizontal = ('clients',) 
    search_fields = ('title', 'special_key')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'surname', 'phone_number', 'reg_date')
    search_fields = ('name', 'surname', 'phone_number')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id_payment', 'id', 'name', 'amount', 'reg_date')
    list_filter = ('id', 'reg_date')
    search_fields = ('name', 'id_payment')

admin.site.register(Client, ClientAdmin)
admin.site.register(DragAndDrop, DragAndDropAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(PayProduct, PayProductAdmin)
admin.site.register(Expense, ExpenseAdmin)
