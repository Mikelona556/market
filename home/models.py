from email.policy import default
from django.db import models

# Create your models here.

class Contact(models.Model):
    STATUS = [
        # ('actual db value', 'admin value')
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Updated', 'Updated'),
        ('Completed', 'Completed'),
    ]

    full_name = models.CharField(max_length= 50)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=50, default= 'New', choices= STATUS)
    sent = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.full_name

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

class Category(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to= 'Category', default= 'adeyemi.jpg')
    slug = models.SlugField(default= '-')

    def _str_(self):
        return self.title      

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    title_r = models.CharField(max_length=50)
    slug = models.SlugField(default= '-')
    img_r = models.ImageField(upload_to = 'Product', default= 'product.jpg')
    description = models.TextField()
    price = models.FloatField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    size = models.IntegerField()
    display = models.BooleanField()
    shoes = models.BooleanField()
    bags = models.BooleanField()
    perfume = models.BooleanField()
    cloth = models.BooleanField()
    uploaded = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.title_r

