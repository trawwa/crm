from django.contrib import admin

from .models import Order, Device, Customer, DeviceInField


class DeviceAdmin(admin.ModelAdmin):
    search_fields = ('manufacturer', 'model')
    list_display = ('id', 'manufacturer', 'model')


class OrderAdmin(admin.ModelAdmin):
    def my_customer(self, obj):
        return obj.device.customer.customer_name
    
    def my_serial_number(self, obj):
        return obj.device.serial_number
    
    def my_device_model(self, obj):
        return obj.device.analyzer.model
    
    def my_device_manufacturer(self, obj):
        return obj.device.analyzer.manufacturer
    
    my_customer.short_description = "Пользователь"
    my_serial_number.short_description = "Серийный номер"
    my_device_model.short_description = 'Модель'
    my_device_manufacturer.short_description = 'Производитель'

    list_display = ('id', 'my_device_manufacturer', 'my_device_model', 'my_serial_number', 
                    'my_customer', 'order_description', 'created_dt', 'last_updated_dt', 'order_status')
    
    search_fields = ()