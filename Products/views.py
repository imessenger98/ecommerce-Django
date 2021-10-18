from Products import models
from Commodity.models import Category, Product
from Vendor.models import Vendors
from .models import addtocart, dbwishlist, order, orderdetails
from .models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import datetime


def homepage(request):
    c = Product.objects.all()
    k = Product.objects.all().order_by('-id')  # recent product
    z = Category.objects.all().values()
    if request.user.is_authenticated:
        y = addtocart.objects.filter(auser=request.user.id).count()
        a = dbwishlist.objects.filter(wuser=request.user.id).count()
    else:
        y = 0
        a = 0
    print(z)
    return render(request, "index.html", {"product": c, "rproduct": k, "nuser": z, "addtocart": y, 'wishlist': a})


def loginuser(request):
    print(request)
    if request.method == "POST":
        print(request)
        em = request.POST.get("Email")
        cl = request.POST.get("Password")
        user = authenticate(request, email=em, password=cl)
        if user:
            login(request, user)
            print("user logged in successfully")
            return redirect("Home")
        else:
            return HttpResponse("invalid user/password")

    return render(request, "Register.html")


def registeruser(request):
    print(request)
    if request.method == "POST":
        firstname = request.POST.get("FName")
        lastname = request.POST.get("LName")
        em = request.POST.get("Email")
        cl = request.POST.get("Password")
        Mobile = request.POST.get("Mobile")
        Adress = request.POST.get("Adress")
        city = request.POST.get("City")
        postcode = request.POST.get("Postcode")
        img = request.FILES["image"]
        f = FileSystemStorage()
        fp = f.save(img.name, img)
        print(img)
        if User.objects.filter(email=em, password=cl).exists():
            return redirect("Home")
        else:
            print("inside else loop")
            try:
                User.objects.create_user(email=em, password=cl, first_name=firstname, last_name=lastname,
                                         phone=Mobile, address=Adress, city=city, postcode=postcode, pic=fp)
                return HttpResponse("account created successfully")
            except Exception as e:
                return HttpResponse("error:user exist please login")

    return render(request, "register.html")


def myaccount(request):
    if request.user.is_authenticated:
        print(request)
        c = order.objects.filter(customer_id__email=request.user.email)
        print(request.user.email)
        print(c)
        if request.user.is_authenticated:
            print(request.user.is_authenticated)
            return render(request, "my-account.html", {"user": c})
        else:
            return render(request, "register.html")
    else:
        return redirect("register")


def signout(request):
    logout(request)
    return redirect("Home")


def update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            firstname = request.POST.get("FName")
            lastname = request.POST.get("LName")
            em = request.POST.get("Email")
            cl = request.POST.get("Password")
            Mobile = request.POST.get("Mobile")
            Adress = request.POST.get("Adress")
            city = request.POST.get("City")
            postcode = request.POST.get("Postcode")
            img = request.FILES["image"]
            print(img.name)
            f = FileSystemStorage()
            fp = f.save(img.name, img)
            print(fp)
            k = User.objects.filter(email=request.user.email)
            k.update(email=em, first_name=firstname, last_name=lastname,
                     phone=Mobile, address=Adress, city=city, postcode=postcode, pic=fp)
            logout(request)
            return redirect('myaccount')
        return redirect('myaccount')
    else:
        return redirect("register")


def viewOrder(request):
    c = order.objects.all()
    m = User.objects.all()
    n = Vendors.objects.all()
    d = Product.objects.all()
    if request.method == "POST":
        # section for order detials
        # input for temperory storing
        Product_Name = request.POST.get("Product_Name")
        quantity = int(request.POST.get("quantity"))
        # get the product name from admin and get detials
        v = Product.objects.get(Product_Name=Product_Name)
        m = Product.objects.filter(Product_Name=Product_Name).values()
        v_price = v.Product_Price  # get price from product
        o_subtotal = int(quantity*v_price)  # findtotal
        p_quantity = int(v.Product_Stock)  # get stock from product
        cprice = p_quantity-quantity  # changing product value after ordering
        # section for order detials
        order_date = request.POST.get("order_date")
        customer_id = request.POST.get("Product_Category")
        l = User.objects.get(email=customer_id)
        vendor_id = request.POST.get("Vender")
        print(vendor_id, customer_id)
        k = Vendors.objects.get(username=vendor_id)
        # order_total=request.POST.get("order_total")      #field disabled
        payment_method = request.POST.get("payment_method")
        payment_status = request.POST.get("payment_status")
        delivery_date = request.POST.get("delivery_date")
        status = request.POST.get("status")
        Is_delivered = request.POST.get("Is_delivered")
        # checkbox Is_delivered false issue solved
        if(Is_delivered == None):
            Is_delivered = False
        if(p_quantity == 0):
            m.update(Product_Stock_Status="false")
            return HttpResponse("product out of stock")
        else:
            if((p_quantity) >= quantity):  # will place order only if product quantity greater than ordered

                x = order.objects.create(order_date=order_date, customer_id=l, vendor_id=k, order_total=o_subtotal, payment_method=payment_method,
                                         payment_status=payment_status, delivery_date=delivery_date, status=status, Is_delivered=Is_delivered)
                orderdetails.objects.create(
                    product_id=v, product_qty=quantity, product_price=v_price, subtotal=o_subtotal, order=x)
                # chaning value of stock product after order completion
                m.update(Product_Stock=cprice)
                return redirect("viewOrder")
            else:
                return HttpResponse("order could not be completed :product required greater than stock")
    return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})


def AddCustomer(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = User.objects.all()
        if request.method == "POST":
            firstname = request.POST.get("FName")
            lastname = request.POST.get("LName")
            em = request.POST.get("Email")
            cl = request.POST.get("Password")
            Mobile = request.POST.get("Mobile")
            Adress = request.POST.get("Adress")
            city = request.POST.get("City")
            postcode = request.POST.get("Postcode")
            img = request.FILES["image"]
            role = request.POST.get("role")
            f = FileSystemStorage()
            fp = f.save(img.name, img)
            if User.objects.filter(email=em, password=cl).exists():
                return HttpResponse("account already exist")
            else:
                print("inside else loop")
                User.objects.create_user(email=em, password=cl, first_name=firstname, last_name=lastname,
                                         phone=Mobile, address=Adress, city=city, postcode=postcode, pic=fp, role=role)
                return HttpResponse("account created successfully")

        return render(request, "dashreg.html", {"regduser": c})
    else:
        return redirect("adminlogin")


def orderDetials(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = orderdetails.objects.all()
        return render(request, "dashorderdet.html", {"key": c})
    else:
        return redirect("adminlogin")


def adminlogin(request):
    if request.method == "POST":
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")
        user = authenticate(request, email=Email, password=Password)
        if(user):
            login(request, user)
            print("i am here", request.user.role)
            if(request.user.role == "admin"):
                return redirect("dash")
            elif(request.user.role == "customer"):
                return redirect("Home")
            elif(request.user.role == "driver"):
                return redirect("dash")
            else:
                return HttpResponse("role not assinged contact admin")
        else:
            return HttpResponse("authetication failed")
    return render(request, "dashadminlogin.html")


def filterbyid(request):
    if request.user.is_authenticated and request.user.role == "admin":
        c = order.objects.all()
        m = User.objects.all()
        n = Vendors.objects.all()
        d = Product.objects.all()
        if request.method == "POST":

            c = order.objects.all()
            m = User.objects.all()
            n = Vendors.objects.all()
            d = Product.objects.all()
            na = request.POST.get("filterbyid").strip()
            ca = request.POST.get("filterordate").strip()
            ma = request.POST.get("searchorder").strip()
            print([na], [ca], [ma])
            # here it begins😒
            if(na == "" and ca == "" and ma == ""):
                print("null filter")
            elif(na != "" and ca == "" and ma == ""):
                c = order.objects.filter(customer_id__email=na)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            elif(na == "" and ca != "" and ma == ""):
                print("line 229")
                c = order.objects.filter(delivery_date=ca)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            elif(na == "" and ca == "" and ma != ""):
                print("line 232")
                c = order.objects.filter(status=ma)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            # filter by id and filterordate
            elif(na != "" and ca != "" and ma == ""):
                print("line 232")
                c = order.objects.filter(
                    customer_id__email=na).filter(delivery_date=ca)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            # filter by id and  status
            elif(na != "" and ca == "" and ma != ""):
                print("line 243")
                c = order.objects.filter(
                    customer_id__email=na).filter(status=ma)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            # filter by date and order
            elif(na == "" and ca != "" and ma != ""):
                print("line 248")
                c = order.objects.filter(status=ma).filter(delivery_date=ca)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            # filter by id,status and date
            elif(na != "" and ca != "" and ma != ""):
                print("line 232")
                c = order.objects.filter(delivery_date=ca).filter(
                    status=ma).filter(customer_id__email=na)
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})
            else:
                return render(request, "dashorder.html", {"product": c, "user": m, "vendors": n, "pr": d})

    else:
        return redirect("adminlogin")


def addingtocart(request, userid):
    if request.user.is_authenticated:
        k = request.user.id
        m = Product.objects.get(id=userid)
        l = User.objects.get(id=k)

        if request.method == "POST":
            j = request.POST.get("quantity")
            print(j)
            addtocart.objects.create(auser=l, aproduct=m, quantity=j)
            return redirect("viewcart")
        else:

            addtocart.objects.create(auser=l, aproduct=m)
            print(k, ":added a product to cart")
            return redirect("viewcart")

    else:
        return redirect("register")


def viewcart(request):
    if request.user.is_authenticated:
        s = 0
        k = request.user.id
        m = User.objects.get(id=k)
        q = addtocart.objects.filter(auser__id=k)
        l = addtocart.objects.filter(auser=m)
        for i in l:
            print(i)
            n = i.aproduct_id
            print("n inte value:", n)
            m = i.quantity
            print(n, m)
            k = Product.objects.get(id=n)
            o = k.Product_Price
            s = s+o*m
        print(s)
        n = None
        print(n)
        return render(request, "viewcart.html", {"product": q, "price": s, "lengt": n})
    else:
        return redirect("register")


def wishlist(request):
    x = []
    if request.user.is_authenticated:
        k = request.user.id
        m = User.objects.get(id=k)
        l = dbwishlist.objects.filter(wuser=m)
        for i in l:
            n = i.wproduct_id
            print(n)
            k = Product.objects.get(id=n)
            print(k)

            x.append(k)
        print(x)
        return render(request, "wishlist.html", {"product": x})
    else:
        return redirect("register")


def addwishlist(request, userid):
    if request.user.is_authenticated:
        k = request.user.id
        m = Product.objects.get(id=userid)
        l = User.objects.get(id=k)
        dbwishlist.objects.create(wuser=l, wproduct=m)
        print(k, ":added a product to wishlist")
        return redirect("wishlist")
    return redirect("register")


def deletecart(request, userid):

    if request.user.is_authenticated:
        n = request.user.id
        m = User.objects.get(id=n)
        o = Product.objects.get(id=userid)
        k = addtocart.objects.filter(aproduct=o).filter(auser=m).first()
        print(k)
        k.delete()
        return redirect("viewcart")
    return redirect("register")


def buynow(request, prid):
    print(prid)
    if request.user.is_authenticated and request.method == "POST":
        k = request.user.id
        quantity = int(request.POST.get("quantity"))
        payment = request.POST.get("payment")
        customer_id = User.objects.get(id=k)
        product = Product.objects.get(id=prid)
        product_fil = Product.objects.filter(id=prid)
        vendor_id = product.product_vendor
        p_quantity = product.Product_Stock
        productprice = product.Product_Price
        order_total = quantity*productprice
        payment_method = payment
        payment_status = False
        print(p_quantity, type(p_quantity))
        print(quantity, type(quantity))

        order_date = datetime.date.today()
        if(p_quantity == 0):
            product_fil.update(Product_Stock_Status=False)
            return HttpResponse("product out of stock")
        else:
            if((p_quantity) >= quantity):

                x = order.objects.create(order_date=order_date, customer_id=customer_id, order_total=order_total,
                                         payment_method=payment_method, payment_status=payment_status, vendor_id=vendor_id)
                current_quanty = p_quantity-quantity
                product_fil.update(Product_Stock=current_quanty)
                orderdetails.objects.create(
                    product_id=product, product_qty=quantity, product_price=productprice, subtotal=order_total, order=x)
                return HttpResponse("order completed successfully")

            else:
                return HttpResponse("order could not be completed :product required greater than stock")

    elif request.user.is_authenticated:
        c = Product.objects.get(id=prid)
        print(c)
        return render(request, "checkout.html", {"product": c})

    else:
        return redirect("register")


def deletewishlist(request, userid):

    if request.user.is_authenticated:
        n = request.user.id
        m = User.objects.get(id=n)
        o = Product.objects.get(id=userid)
        k = dbwishlist.objects.filter(wproduct=o).filter(wuser=m).first()
        print(k)
        k.delete()
        return redirect("wishlist")
    return redirect("register")


def checkout(request):
    if request.user.is_authenticated:
        k = request.user.id
        k = User.objects.get(id=k)
        c = addtocart.objects.filter(auser=k)
        print(c)
        for i in c:
            print("i am inside loop")
            quantity = int(i.quantity)
            payment = "cod"
            customer_id = i.auser
            product = Product.objects.get(Product_Name=i.aproduct)
            product_fil = Product.objects.filter(id=product.id)
            print(product, product_fil)
            print("444")
            vendor_id = product.product_vendor
            p_quantity = product.Product_Stock
            productprice = product.Product_Price
            order_total = quantity*productprice
            payment_method = payment
            payment_status = False
            print(p_quantity, type(p_quantity))
            print(quantity, type(quantity))
            print("453")
            order_date = datetime.date.today()
            if(p_quantity == 0):
                product_fil.update(Product_Stock_Status=False)
                return HttpResponse("product out of stock")
            else:
                if((p_quantity) >= quantity):

                    x = order.objects.create(order_date=order_date, customer_id=customer_id, order_total=order_total,
                                             payment_method=payment_method, payment_status=payment_status, vendor_id=vendor_id)
                    current_quanty = p_quantity-quantity
                    product_fil.update(Product_Stock=current_quanty)
                    orderdetails.objects.create(
                        product_id=product, product_qty=quantity, product_price=productprice, subtotal=order_total, order=x)

                else:
                    return HttpResponse("order could not be completed :product required greater than stock")
        addtocart.objects.all().delete()
        return HttpResponse("order completed successfully")

    return redirect("register")
