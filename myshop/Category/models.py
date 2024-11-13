from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    specifications = models.JSONField()
