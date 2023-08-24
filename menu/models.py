from django.db import models


# Create your models here.

class MenuItem(models.Model):
    food_name = models.CharField(max_length=200)
    kitchen = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    volume = models.PositiveSmallIntegerField(blank=True, null=True)
    published = models.BooleanField(default=False)

    # dates // for manager not for customers
    created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return f'{self.food_name}'


class Menu(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
