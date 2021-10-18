from os import name
from Products.views import AddCustomer
from django.contrib import admin
from django.urls import path
from Commodity import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
#product    
    path('admins',views.dashBoard,name="dash"),
    path('addcomm',views.addCommodity,name='addcomm'),
    path('viewcomm',views.viewCommodity,name='viewcomm'),
    path('updatecomm<int:userid>',views.updateCommodity,name='updatecomm'),
    path("delete<int:userid>",views.delete,name='deletedata'),
#category
    path('addcat',views.addcat,name='addcat'),
    path('viewcat',views.viewcat,name='viewcat'),
    path('updatecat<int:userid>',views.updatecat,name='updatecat'),
    path('status',views.status,name="status"),
    path("productdetials",views.productdetials,name="productdetials"),
    path("realproductdetial<int:userid>",views.realproductdetial,name="realproductdetial"),
    path("searchwith",views.searchwith,name="searchwith"),
    path("updatepass",views.updatepass,name="updatepass"),
    path("categoryname<int:userid>",views.categoryname,name="categoryname")
  
] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
