from django.contrib import admin
from .models import addtocart, dbwishlist, orderdetails
from .models import User
from .models import order
admin.site.register(User)
admin.site.register(order)
admin.site.register(orderdetails)
admin.site.register(addtocart)
admin.site.register(dbwishlist)
