from django.db import models


class Post(models.Model):
    date = models.DateTimeField('date published')
    photo = models.TextField()


class PizzaCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    size = models.PositiveIntegerField(default=30)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    is_custom_pizza = models.BooleanField(default=False)

    def __str__(self):
        return self.name
