from django.db import models

# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class ShopEmail(models.Model):
    shop = models.ForeignKey(Shop, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email

class ShopPhone(models.Model):
    shop = models.ForeignKey(Shop, related_name='phones', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone

