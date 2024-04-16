from django.db import models
from django.conf import settings

class Product(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	price = models.IntegerField()
	image = models.ImageField(upload_to="images/", blank=True)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products'
	)
	like_users = models.ManyToManyField(
		settings.AUTH_USER_MODEL, related_name="like_products"
	)

	def __str__(self):
		return self.title
	
