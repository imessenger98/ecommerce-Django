from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from Vendor import views
urlpatterns = [
    path('vendor',views.viewVendor,name="vendor")
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
