
# Django
from django.contrib import admin

# local Django
from .models import Category, Donation, Institution

# Register your models here.


admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
