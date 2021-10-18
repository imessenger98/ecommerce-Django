from Vendor.models import Vendors
from django.shortcuts import render
from django.http import request
from django.http.response import HttpResponse,HttpResponseRedirect

def viewVendor(request):
    c=Vendors.objects.all()
    if request.method == "POST":
        branch=request.POST.get("branch")
        vendor_name=request.POST.get("vendor_name")
        phone_number=request.POST.get("phone_number")
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        address=request.POST.get("address")
        Vendors.objects.create(branch=branch,vendor_name=vendor_name,phone_number=phone_number,email=email,username=username,password=password,address=address)
        return render(request,"dashvendor.html",{"vendor":c})
    return render(request,"dashvendor.html",{"vendor":c})

