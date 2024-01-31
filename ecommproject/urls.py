"""
URL configuration for ecommproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("loginuser/", views.loginuser, name="loginuser"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("registeruser/", views.registeruser, name="registeruser"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("contactus", views.contactus, name="contactus"),
    path("mobilelistview", views.mobilelistview, name="mobilelistview"),
    path("clothslistview", views.clothslistview, name="clothslistview"),
    path("shoeslistview", views.shoeslistview, name="shoeslistview"),
    path("range_view", views.range_view, name="range_view"),
    path("allsortedorderview", views.allsortedorderview, name="allsortedorderview"),
    path("searchproduct", views.searchproduct, name="searchproduct"),
    path("cart", views.cart, name="cart"),
    path("addtocart/<product_id>", views.addtocart, name="addtocart"),
    path("removecart/<product_id>", views.removecart, name="removecart"),
    path("updateqty/<qv>/<product_id>", views.updateqty, name="updateqty"),
    path("placeorder", views.placeorder, name="placeorder"),
    path("payment", views.payment, name="payment"),
    path("showorders", views.showorders, name="showorders"),
    path("registerproduct", views.registerproduct, name="registerproduct"),
    path("viewregisterproduct", views.viewregisterproduct, name="viewregisterproduct"),
    path(
        "deleteregisterproduct/<product_id>",
        views.deleteregisterproduct,
        name="deleteregisterproduct",
    ),
    path(
        "updateproducts/<product_id>",
        views.updateproducts,
        name="updateproducts",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
