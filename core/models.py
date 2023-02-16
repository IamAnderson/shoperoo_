from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255)


	class Meta:
		ordering = ('name',)
		verbose_name_plural = "Categories"

	def __str__(self):
		return str(self.name)



class Item(models.Model):
	category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	price = models.FloatField()
	image = models.ImageField(upload_to="item_image", blank=True, null=True)
	is_sold = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
	created_at= models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.name)

class Messages(models.Model):
	item = models.ForeignKey(Item, related_name='messages', on_delete=models.CASCADE)
	members = models.ManyToManyField(User, related_name='messages')
	created_at= models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-modified_at', )
	def __str__(self):
		return str(self.members)

class Convo(models.Model):
	conversation = models.ForeignKey(Messages , related_name='convo', on_delete=models.CASCADE)
	content = models.TextField()
	created_at= models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User , related_name='created_message', on_delete=models.CASCADE)
	def __str__(self):
		return str(self.content)

class Cart(models.Model):
	item = models.ForeignKey(Item, related_name='cart_item', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='cart_user', on_delete=models.CASCADE)
	def __str__(self):
		return str(self.item)


class History(models.Model):
	item = models.ForeignKey(Item, related_name='past_purchase', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
	def __str__(self):
		return str(self.item)
