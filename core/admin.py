from django.contrib import admin
from .models import Category,Item,Messages, Convo,Cart,History


# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Messages)
admin.site.register(Convo)
admin.site.register(Cart)
admin.site.register(History)