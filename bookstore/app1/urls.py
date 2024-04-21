from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('adminPanel/',views.adminPanel, name="adminPanel"),
    path('home/',views.home, name="home"),
    path('logout/', views.logout, name="logout"),
    path('adminProduct/',views.adminProduct,name="adminProduct"),
    path('adminProduct/<int:proId>/<str:action>/',views.updatePro,name="updatePro"),
    path('adminProduct/<str:action>/<int:prodId>/',views.deletePro,name="deletePro"),
    path('adminOrders/',views.adminOrders,name="adminOrders"),
    path('adminOrders/<int:ordId>/',views.deleteOrder,name="deleteOrder"),
    path('adminUsers/',views.adminUsers,name="adminUsers"),
    path('adminUsers/<int:uId>/',views.deleteUser,name="deleteUser"),
    path('adminContacts',views.adminContacts,name="adminContacts"),
    path('adminContacts/<int:messId>/',views.deleteContact,name="deleteContact"),
    path('about/',views.about,name="about"),
    path('shop/',views.shop,name="shop"),
    path('contact/',views.contact,name="contact"),
    path('cart/',views.cart,name="cart"),
    path('cart/<int:cId>/',views.deleteCart,name="deleteCart"),
    path('cart/<str:action>/<int:myId>/',views.deleteAllCart,name="deleteAllCart"),
    path('checkout/',views.checkout,name="checkout"),
    path('orders/',views.orders,name="orders"),
    path('search/',views.search,name="search")
]