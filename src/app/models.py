from django.db import models


class Post(models.Model):
    date = models.DateTimeField('date published')
    photo = models.TextField()


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    size = models.PositiveIntegerField(default=30)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    #image = models.ImageField(upload_to="gallery", default="https://source.unsplash.com/random/400x400")
    image = models.ImageField(upload_to="gallery", blank=True)
    is_custom_pizza = models.BooleanField(default=False)
    #todo legyen default image ne legyen kotelezo
    def __str__(self):
        return self.name
