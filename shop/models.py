from django.db import models
from .tests import BadRequest
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
# Create your models here.

# User table
class User(AbstractUser):
    phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
    username = models.CharField(_('Username'), unique=True,max_length=15, blank=True, null=True)
    email = models.EmailField(_('Email Address'), null=True, blank=True)
    password = models.CharField(_('Password'), max_length=155, null=True, blank=True)
    latitude = models.DecimalField(_('work_location_lat'), default=0, null=False, decimal_places=15,
                                            max_digits=20)
    longitude = models.DecimalField(_('work_location_lat'), default=0, null=False, decimal_places=15,
                                            max_digits=20) 
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

# Shops table
class Shop(models.Model):
    shop_name = models.CharField(_('Shop Name'),max_length=50,null=True,blank=True)
    shop_address = models.CharField(_('Address'),max_length=155,null=True,blank=True)
    latitude = models.DecimalField(_('work_location_lat'), default=0, null=False, decimal_places=15,
                                            max_digits=20)
    longitude = models.DecimalField(_('work_location_lat'), default=0, null=False, decimal_places=15,
                                            max_digits=20)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True, db_index=True)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    class Meta:
        db_table = 'shop_data'
        verbose_name = 'shop_data'
        verbose_name_plural = 'shop_data'
        managed = True

    def __str__(self):
        return f"{self.shop_name}"

class ShopReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=False)
    shop_review = models.CharField(_('Review'),max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True, db_index=True)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    class Meta:
        db_table = 'shop_review'
        verbose_name = 'shop_review'
        verbose_name_plural = 'shop_review'
        managed = True

    def __str__(self):
        return f"{self.shop_review}"