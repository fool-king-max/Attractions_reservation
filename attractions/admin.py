from django.contrib import admin

# Register your models here.
# 在 attractions/admin.py 中
from .models import *

admin.site.register(Attraction)
admin.site.register(Province)
admin.site.register(Reservation)
admin.site.register(Review)