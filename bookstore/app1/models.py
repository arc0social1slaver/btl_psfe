from django.db import models
from django.db.models import *
from django.template.defaulttags import register

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name
    @property
    def totalNormalUser(self):
        return Users.objects.filter(user_type="user").count()
    @property
    def totalNormalAdmin(self):
        return Users.objects.filter(user_type="admin").count()
    
class Cart(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'cart'
    
    def __str__(self):
        return self.name
    @property
    def subTotal(self):
        return self.price * self.quality

class Message(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'message'
    
    def __str__(self):
        return self.name
    


class Orders(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    total_products = models.CharField(max_length=1000, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    placed_on = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.name
    @property
    def total_pendings(self):
        if Orders.objects.filter(payment_status='pending').aggregate(TOTAL = Sum('total_price'))["TOTAL"] == None:
            return 0
        return Orders.objects.filter(payment_status='pending').aggregate(TOTAL = Sum('total_price'))["TOTAL"]
    @property
    def total_compls(self):
        if Orders.objects.filter(payment_status='completed').aggregate(TOTAL = Sum('total_price'))["TOTAL"] == None:
            return 0
        return Orders.objects.filter(payment_status='completed').aggregate(TOTAL = Sum('total_price'))["TOTAL"]
    


class Products(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name
    