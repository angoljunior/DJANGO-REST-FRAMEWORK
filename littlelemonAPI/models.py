from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)


class MenuItem(models.Model):
    title       = models.CharField(max_length=255)
    price       = models.DecimalField(max_digits=6,decimal_places=2,default=0,null=True, blank=True)
    inventory   = models.SmallIntegerField(default=0,null=True, blank=True)
    category    = models.ForeignKey(Category ,on_delete=models.PROTECT,default=None)

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem    = models.ForeignKey(MenuItem ,on_delete=models.CASCADE)
    quantity    = models.ForeignKey(MenuItem, on_delete=models.CASCADE,related_name='no_of_items',null=True, blank=True)
    unit_price  = models.DecimalField(max_digits=6,decimal_places=2,null=True, blank=True)
    price       = models.DecimalField(max_digits=6,decimal_places=2,null=True, blank=True)

    class Meta:
        unique_together = ('menuitem','price') #tuple 

class Order(models.Model):
    user          = models.ForeignKey(User ,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="delivery_crew", null=True)
    status        = models.BooleanField(db_index=True,default=0,null=True, blank=True)
    total         =models.DecimalField(max_digits=6,decimal_places=2,null=True, blank=True)
    date          = models.DateField(db_index=True,null=True, blank=True)


class OrderItem(models.Model):
    order       = models.ForeignKey(User,on_delete=models.CASCADE)
    menuitem    = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity    = models.SmallIntegerField()
    unit_price  = models.DecimalField(max_digits=6,decimal_places=2)
    price       = models.DecimalField(max_digits=6,decimal_places=2)
     
    class Meta:
        unique_together = ['menuitem','price']  #list #for two unique indexes