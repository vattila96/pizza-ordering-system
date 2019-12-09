from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE)
# Todo change hard-coded allergens to a new Class in the DB
    contains_milk = models.BooleanField(default=False)
    contains_peanuts = models.BooleanField(default=False)
    contains_gluten = models.BooleanField(default=False)
    contains_fish = models.BooleanField(default=False)
    contains_wheat = models.BooleanField(default=False)

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="gallery", blank=True)
    is_custom_pizza = models.BooleanField(default=False)

    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=128, default='M')
    birthday = models.DateField(null=True, blank=True)
    newsletter = models.BooleanField(default=True)
    address_main = models.CharField(max_length=256, null=True, blank=True)
    address_secondary = models.CharField(max_length=256, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
