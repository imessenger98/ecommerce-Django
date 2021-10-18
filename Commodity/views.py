from numpy import product
from Products.models import User, order, orderdetails
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Product
from .models import Category
from .models import Vendors
import pandas as pd
import os
# get directory name from specified path and the specitfied path is os.path.abspath(__file__)) syntax:os.path.dirname()
# manage.py olla path return cheyyum
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
# product


def dashBoard(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = Product.objects.all().count()
        d = User.objects.all().count()
        e = order.objects.all().count()
        return render(request, "dasboardindex.html", {"1product": c, "1user": d, "1order": e})
    else:
        return redirect("adminlogin")


def addCommodity(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = Category.objects.all()
        v = Vendors.objects.all()
        if request.method == "POST":
            print(request.POST)
            print("hi iam here")
            Product_Name = request.POST.get("Product_Name")
            Product_Discription = request.POST.get("Product_Discription")
            Product_Price = request.POST.get("Product_Price")
            Product_Stock = request.POST.get("Product_Stock")
            Product_Stock_Status = request.POST.get("Product_Stock_Status")
            Product_cat = request.POST.get("Product_Category")
            product_vendor = request.POST.get("vendor_name")
            print(product_vendor)
            Product_Category = Category.objects.get(Category_Name=Product_cat)
            Product_Image = request.FILES["Product_Image"]
            product_vendor = Vendors.objects.get(vendor_name=product_vendor)
            print(product_vendor)
            f = FileSystemStorage()
            fp = f.save(Product_Image.name, Product_Image)
            Product.objects.create(Product_Name=Product_Name, Product_Discription=Product_Discription, Product_Price=Product_Price, Product_Stock=Product_Stock,
                                   Product_Stock_Status=Product_Stock_Status, Product_Category=Product_Category, Product_Image=fp, product_vendor=product_vendor)
            return redirect("viewcomm")
        return render(request, "dashadd.html", {'cat': c, 'vendor': v})
    else:
        return redirect("adminlogin")


def viewCommodity(request):
    if request.user.is_authenticated and request.user.role == "admin":
        k = Product.objects.all()
        df = pd.DataFrame(k.values())
        print(df)
        path = os.path.join(BASE_DIR, 'media/csvfile/products.csv')
        df.to_csv(path)
        print(BASE_DIR)
        if request.method == "POST":
            search = request.POST.get("search")
            flexRadio = request.POST.get("flexRadio")
            if(flexRadio == "Category"):
                f = Product.objects.filter(
                    Product_Category__Category_Name=search)
                df = pd.DataFrame(f.values())
                print(df)
                df.to_csv(path)
                return render(request, "dashview.html", {'product': f})
            if(flexRadio == "Product_Name"):
                f = Product.objects.filter(Product_Name=search)
                df = pd.DataFrame(f.values())
                print(df)
                print("i am here")
                df.to_csv(path)
                return render(request, "dashview.html", {'product': f})
        c = Product.objects.all()
        return render(request, "dashview.html", {"product": c})
    else:
        return redirect("adminlogin")


def updateCommodity(request, userid):
    if request.user.is_authenticated and request.user.role == "admin":
        c = Category.objects.all()
        k = Product.objects.filter(id=userid).values()
        if request.method == "POST":
            print(request.POST)
            print("hi iam here")
            Product_Name = request.POST.get("Product_Name")
            Product_Discription = request.POST.get("Product_Discription")
            Product_Price = request.POST.get("Product_Price")
            Product_Stock = request.POST.get("Product_Stock")
            Product_Stock_Status = request.POST.get("Product_Stock_Status")
            Product_cat = request.POST.get("Product_Category")
            Product_Category = Category.objects.get(Category_Name=Product_cat)
            Product_Image = request.FILES["Product_Image"]
            f = FileSystemStorage()
            fp = f.save(Product_Image.name, Product_Image)
            k = Product.objects.filter(id=userid).values()
            k.update(Product_Name=Product_Name, Product_Discription=Product_Discription, Product_Price=Product_Price,
                     Product_Stock=Product_Stock, Product_Stock_Status=Product_Stock_Status, Product_Category=Product_Category, Product_Image=fp)
            return redirect("viewcomm")
        return render(request, "dashupdate.html", {"product": k[0], "id": userid, "cat": c})
    else:

        return redirect("adminlogin")


def delete(request, userid):
    if request.user.is_authenticated and request.user.role == "admin":
        k = Product.objects.filter(id=userid)
        k.delete()
        return redirect("viewcomm")
    else:
        return redirect("adminlogin")

# category


def addcat(request):
    if request.user.is_authenticated and request.user.role == "admin":
        if request.method == "POST":
            print(request.POST)
            print("hi i am inside addcat")
            Category_Name = request.POST.get("Category_Name")
            Category_Discription = request.POST.get("Category_Discription")
            k = Category.objects.filter(Category_Name=Category_Name).exists()
            if not k:
                Category.objects.create(
                    Category_Name=Category_Name, Category_Discription=Category_Discription)
                return HttpResponse("added successfully")
            if k:
                return HttpResponse("category already exist")
        return render(request, "dashaddcat.html")
    else:

        return redirect("adminlogin")


def viewcat(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = Category.objects.all()
        return render(request, "dashviewcat.html", {"category": c})
    else:

        return redirect("adminlogin")


def updatecat(request, userid):
    if request.user.is_authenticated and request.user.role == "admin":
        k = Category.objects.filter(id=userid).values()
        print(k)
        if request.method == "POST":
            print(request.POST)
            print("hi iam here")
            Category_Name = request.POST.get("Category_Name")
            Category_Discription = request.POST.get("Category_Discription")
            # GET THE OBJECT AND THEN  CALLING IT TO UPDATE
            k.update(Category_Discription=Category_Discription,
                     Category_Name=Category_Name)
            return redirect("viewcat")
        return render(request, "dashupdatecate.html", {"category": k[0], "id": userid})
    else:
        return redirect("adminlogin")


def status(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = Product.objects.all().count()
        d = User.objects.all().count()
        e = order.objects.all().count()
        f = Vendors.objects.all().count()
        return render(request, "dashstatus.html", {"1product": c, "1user": d, "1order": e, "vendor": f})
    else:
        return redirect("adminlogin")


def productdetials(request):
    a = Category.objects.all()
    c = Product.objects.all()
    return render(request, "product-list.html", {"product": c, 'category': a})


def realproductdetial(request, userid):
    if request.user.is_authenticated:
        a = Category.objects.all()
        k = Product.objects.get(id=userid)
        l = k.Product_Category
        print(l)
        m = Product.objects.filter(Product_Category__Category_Name=l)
        print(m, a)
        return render(request, "product-detail.html", {"user": k, 'recent': m, 'category': a})
    else:
        return redirect("register")


def searchwith(request):
    c = Category.objects.all()
    if request.method == "POST":
        Product_Name = request.POST.get("Product_Name")
        k = Product.objects.filter(Product_Name__startswith=Product_Name)
        m = Product.objects.filter(
            Product_Name__startswith=Product_Name).count()
        if(m == 0):
            x = Category.objects.filter(
                Category_Name__startswith=Product_Name).first()
            print(x)
            print("i am here")
            k = Product.objects.filter(Product_Category=x)
        return render(request, "product-list.html", {"product": k, 'category': c})


def categoryname(request, userid):
    print(userid)
    c = Product.objects.filter(Product_Category__id=userid)
    print(c)
    return render(request, "product-list.html", {"product": c})


def updatepass(request):
    if request.user.is_authenticated and request.method == "POST":
        m = request.user.id
        k = User.objects.filter(id=m)
        password = request.POST.get("password")
        k.update(password=password)
        return redirect("myaccount")

    else:
        return redirect("register")
