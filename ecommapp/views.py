from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order

# Create your views here.


def index(req):
    username = req.user.username
    allproducts = Product.objects.all()
    context = {"username": username, "allproducts": allproducts}
    return render(req, "index.html", context)


def userlogout(req):
    logout(req)
    return redirect("/")


def loginuser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "loginuser.html", context)
        else:
            username = uname
            userdata = authenticate(username=uname, password=upass)
            context = {"username": username}
            if userdata is not None:
                login(req, userdata)
                return redirect("/")
                # return render(req, "index.html", context)
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "loginuser.html", context)
    else:
        return render(req, "loginuser.html")


def registeruser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "registeruser.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and Confirm Password doesn't match"
            return render(req, "registeruser.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/")
            except Exception:
                context["errmsg"] = "User Already Exists"
                return render(req, "registeruser.html", context)
    else:
        return render(req, "registeruser.html")


def aboutus(req):
    if req.user.is_authenticated:
        user = req.user
        context = {"username": user}
        return render(req, "aboutus.html", context)
    else:
        return render(req, "aboutus.html")


def contactus(req):
    if req.user.is_authenticated:
        user = req.user
        context = {"username": user}
        return render(req, "contactus.html", context)
    else:
        return render(req, "contactus.html")


def mobilelistview(req):
    if req.method == "GET":
        allproducts = Product.prod.mobile_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def clothslistview(req):
    if req.method == "GET":
        allproducts = Product.prod.cloths_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def shoeslistview(req):
    if req.method == "GET":
        allproducts = Product.prod.shoes_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def range_view(req):
    if req.method == "GET":
        return render(req, "index.html")
    else:
        r1 = req.POST.get("min")
        r2 = req.POST.get("max")
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts = Product.prod.get_price_range(r1, r2)
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)
        else:
            allproducts = Product.objects.all()
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)


def allsortedorderview(req):
    sort_option = req.GET.get("sort")
    if sort_option == "high_to_low":
        allproducts = Product.objects.order_by("-price")
    elif sort_option == "low_to_high":
        allproducts = Product.objects.order_by("price")
    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts}
    return render(req, "index.html", context)


from django.db.models import Q


def searchproduct(req):
    query = req.GET.get("q")
    errmsg = ""
    if query:
        allproducts = Product.objects.filter(
            Q(product_name__icontains=query)
            | Q(category__icontains=query)
            | Q(price__icontains=query)
            | Q(desc__icontains=query)
        )
        # print(len(allproducts))
        if len(allproducts) == 0:
            errmsg = "No result found"

    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts, "query": query, "errmsg": errmsg}
    return render(req, "index.html", context)


def cart(req):
    if req.user.is_authenticated:
        username = req.user.username
        allcarts = Cart.objects.filter(userid=req.user.id)
        totalprice = 0
        for x in allcarts:
            totalprice = totalprice + x.product_id.price * x.qty
        length = len(allcarts)
        context = {
            "username": username,
            "allcarts": allcarts,
            "total": totalprice,
            "items": length,
        }
        return render(req, "cart.html", context)
    else:
        allcarts = Cart.objects.filter(userid=req.user.id)
        totalprice = 0
        for x in allcarts:
            totalprice = totalprice + x.product_id.price * x.qty
        length = len(allcarts)
        context = {
            "allcarts": allcarts,
            "total": totalprice,
            "items": length,
        }
        return render(req, "cart.html", context)


def addtocart(req, product_id):
    if req.user.is_authenticated:
        user = req.user
    else:
        user = None

    allproducts = get_object_or_404(Product, product_id=product_id)
    cartitem, created = Cart.objects.get_or_create(product_id=allproducts, userid=user)
    if not created:
        cartitem.qty += 1
    else:
        cartitem.qty = 1

    cartitem.save()
    return redirect("/cart")


def removecart(req, product_id):
    cartitem = Cart.objects.filter(product_id=product_id)
    cartitem.delete()
    return redirect("/cart")


def updateqty(req, qv, product_id):
    allcarts = Cart.objects.filter(product_id=product_id)
    if qv == "1":
        total = allcarts[0].qty + 1
        allcarts.update(qty=total)
    else:
        if allcarts[0].qty > 1:
            total = allcarts[0].qty - 1
            allcarts.update(qty=total)
        else:
            allcarts = Cart.objects.filter(product_id=product_id)
            allcarts.delete()

    return redirect("/cart")


def placeorder(req):
    if req.user.is_authenticated:
        user = req.user
    else:
        user = None

    allcarts = Cart.objects.filter(userid=user)
    totalprice = 0
    for x in allcarts:
        totalprice = totalprice + x.product_id.price * x.qty
    length = len(allcarts)
    context = {
        "username": user,
        "allcarts": allcarts,
        "total": totalprice,
        "items": length,
    }
    return render(req, "placeorder.html", context)


import razorpay

import random
from django.conf import settings
from django.core.mail import send_mail


def payment(req):
    if req.user.is_authenticated:
        user = req.user
        client = razorpay.Client(
            auth=("rzp_test_V74TGgEvVi6oSj", "yauJGHyyl1pYKJYJcZlmcYT2")
        )
        # orderid = random.randrange(1000, 9000)
        allcarts = Cart.objects.filter(userid=user)
        for x in allcarts:
            orderid = random.randrange(1000, 9000)
            orderdata = Order.objects.create(
                orderid=orderid, product_id=x.product_id, qty=x.qty, userid=x.userid
            )
            orderdata.save()
            x.delete()
        total_price = 0
        orderdata = Order.objects.filter(userid=user)
        for x in orderdata:
            total_price = total_price + x.product_id.price * x.qty
            oid = x.orderid

        data = {"amount": total_price * 100, "currency": "INR", "receipt": str(oid)}
        payment = client.order.create(data=data)
        subject = "EKart-Payment Status"
        message = f"Hi {user}, Thank you using our services\n Total Amount Paid={total_price} Rs/-"
        emailfrom = settings.EMAIL_HOST_USER
        receiver = [user]
        send_mail(subject, message, emailfrom, receiver)
        context = {"username": user, "data": payment, "amount": payment}
        return render(req, "payment.html", context)
    else:
        user = None
        return redirect("/loginuser")


def showorders(req):
    if req.user.is_authenticated:
        user = req.user
        allorders = Order.objects.filter(userid=user)
        totalprice = 0
        for x in allorders:
            totalprice = totalprice + x.product_id.price * x.qty
        length = len(allorders)
        context = {
            "username": user,
            "allorders": allorders,
            "total": totalprice,
            "items": length,
        }
        return render(req, "showorders.html", context)
    else:
        user = None
        return redirect("/loginuser")


from ecommapp.forms import ViewProduct


def registerproduct(req):
    if req.user.is_authenticated:
        user = req.user
        if req.method == "GET":
            form = ViewProduct()
            return render(req, "registerproduct.html", {"form": form, "username": user})
        else:
            form = ViewProduct(req.POST, req.FILES or None)
            if form.is_valid():
                form.save()
                return redirect("/")
            else:
                return render(
                    req, "registerproduct.html", {"form": form, "username": user}
                )
    else:
        return redirect("/loginuser")


def viewregisterproduct(req):
    if req.user.is_authenticated:
        user = req.user
        myproducts = Product.objects.filter(userid=user)
        context = {"myproducts": myproducts, "username": user}
        return render(req, "viewregisterproduct.html", context)
    else:
        user = None
        return redirect("/loginuser")


def deleteregisterproduct(req, product_id):
    if req.user.is_authenticated:
        user = req.user
        myproducts = Product.objects.filter(userid=user, product_id=product_id)
        myproducts.delete()
        context = {"myproducts": myproducts, "username": user}
        return render(req, "viewregisterproduct.html", context)
    else:
        user = None
        return redirect("/loginuser")


def updateproducts(req, product_id):
    if req.user.is_authenticated:
        user = req.user
        myproducts = get_object_or_404(Product, product_id=product_id)
        if req.method == "POST":
            form = ViewProduct(req.POST, req.FILES, instance=myproducts)
            if form.is_valid():
                form.save()
                return redirect("/viewregisterproduct")
        else:
            form = ViewProduct(instance=myproducts)

        context = {"form": form, "data": [myproducts], "username": user}
        return render(req, "updateproducts.html", context)
    else:
        return redirect("/loginuser")
