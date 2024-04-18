from django.db import models
from django.conf import settings


class Hashtag(models.Model):
    content = models.TextField(unique=True)

    def __str__(self):
        return self.content


class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(
        upload_to="images/", blank=True, default='default')
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def update_counter(self):
        self.view = self.view + 1
        self.save()
