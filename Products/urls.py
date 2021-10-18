from django.contrib import admin
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from Products import views
from django.conf.urls.static import static
from django.conf import settings
from Products import ApiVews

urlpatterns = [
    path('', views.homepage, name="Home"),
    path("login", views.loginuser, name="login"),
    path("myaccount", views.myaccount, name="myaccount"),
    path("logout", views.signout, name="signout"),
    path("registeruser", views.registeruser, name="register"),
    path('update', views.update, name='update'),
    path('vieworder', views.viewOrder, name='viewOrder'),
    path("addcustomer", views.AddCustomer, name="addcustomer"),
    path("orderdetials", views.orderDetials, name="orderdetials"),
    path("adminlogin", views.adminlogin, name="adminlogin"),
    path('filterbyid', views.filterbyid, name='filterbyid'),
    path("showallusers", ApiVews.showallusers),
    path("showallorders", ApiVews.showallorders),
    path("adddatas", ApiVews.addcustomer),
    path("deletecustomer<str:param>", ApiVews.deletecustomer),
    path("updatecustomer<str:param>", ApiVews.updatecustomer),
    path("signup", ApiVews.sugnup),
    path("addingtocart<int:userid>", views.addingtocart, name='addingtocart'),
    path("viewcart", views.viewcart, name='viewcart'),
    path("wishlist", views.wishlist, name='wishlist'),
    path("addwishlist<int:userid>", views.addwishlist, name='addwishlist'),
    path("deletecart<int:userid>", views.deletecart, name='deletecart'),
    path("deletewishlist<int:userid>",
         views.deletewishlist, name='deletewishlist'),
    path("buynow<int:prid>", views.buynow, name='buynow'),
    path("checkout", views.checkout, name='checkout'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
