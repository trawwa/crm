from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.db import models
from datetime import datetime


class Device(models.Model):
    """Оборудование"""

    class Meta:
        db_table = "devices"
        verbose_name = "Доступное оборудование"
        verbose_name_plural = "Доступное оборудование"

    manufacturer = models.TextField(verbose_name="Vendor")
    model = models.TextField(verbose_name="Model")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"
    

class Customer(models.Model):
    """Конечные пользователи оборудования"""

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагента"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_adress = models.TextField(verbose_name="Адрес")
    customer_city = models.TextField(verbose_name="Город")

    def __str__(self):
        return f"{self.customer_name} по адресу {self.customer_adress}"
    

class DeviceInField(models.Model):
    """Оборудование в полях"""

    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Описание в полях"
        verbose_name_plural = "Описание в полях"

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Пользователь")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Оборудование")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.analyzer} с/н {self.serial_number} в {self.customer}"
    

class Order(model.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    statuses = (('open', 'открыта'),
                ('closed', 'закрыта'),
                ('in progress', 'в работе'),
                ('need info', 'нужна информация'),)
    
    device = models.ForeignKey(DeviceInField, on_delete=models.RESTRICT, verbose_name="Оборудование")
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_dt = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", choises=statuses)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"
    
    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)