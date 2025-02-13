from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import date
# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        upass = request.POST.get('password')
        ucpass = request.POST.get('cpassword')
        utype = request.POST.get('user_type')
        checkExist = Users.objects.filter(name=uname,email=uemail,password=upass).count()
        if checkExist > 0:
            context = {'message' : 'The user already exists!'}
            return render(request, 'register.html', context)
        elif upass != ucpass:
            context = {'message' : 'The password does not match!'}
            return render(request, 'register.html', context)
        else:
            newUser = Users(name=uname,email=uemail,password=upass,user_type=utype)
            newUser.save()
            return redirect(login)
    return render(request, 'register.html', {})
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        upass = request.POST.get('password')
        personLogin = Users.objects.filter(name=uname,email=uemail,password=upass)
        checkExist = personLogin.count()
        if checkExist > 0:
            validPerson = personLogin.values()
            if validPerson.count() > 1:
                context = {'message': 'Something wrong happened'}
                return render(request, 'login.html',context)
            else:
               if validPerson[0]['user_type'] == 'user':
                   request.session['user_name'] = uname
                   request.session['user_email'] = uemail
                   request.session['user_id'] = validPerson[0]['id']
                   request.session['loginType'] = validPerson[0]['user_type']
                   return redirect(home)
               else:
                   request.session['admin_name'] = uname
                   request.session['admin_email'] = uemail
                   request.session['admin_id'] = validPerson[0]['id']
                   request.session['loginType'] = validPerson[0]['user_type']
                   return redirect(adminPanel)
        else:
            context = {'message': 'Invalid account!'}
            return render(request, 'login.html',context)
    return render(request, 'login.html', {})
def logout(request):
    try:
        if request.session['loginType'] == 'user':
            del request.session['user_name']
            del request.session['user_email']
            del request.session['user_id']
            del request.session['loginType']
        else:
            del request.session['admin_name']
            del request.session['admin_email']
            del request.session['admin_id']
            del request.session['loginType']
    except:
        return redirect(login)
    return redirect(login)
def adminPanel(request):
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_orders = Orders.objects.all()
        many_products = Products.objects.all()
        many_users = Users.objects.all()
        many_messages = Message.objects.all()
        context = {'current_user':[current_user_name, current_user_email],
                   'many_orders':many_orders, 
                   'many_products': many_products,
                   'many_users': many_users,
                   'many_messages': many_messages
                   }
        return render(request, 'admin-page.html', context)
    else:
        return redirect(login)
def home(request):
    if request.method == 'POST':
        pro_name = request.POST.get("pro_name")
        pro_price = request.POST.get("pro_price")
        pro_quantity = request.POST.get("pro_quantity")
        u_id = request.session['user_id']
        checkExit = Cart.objects.filter(user_id=u_id,name=pro_name).count()
        if checkExit > 0:
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()[:6]
            myCarts = Cart.objects.filter(user_id=current_user_id)
            many_products = Products.objects.all()
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products,
                   'message': 'Product already add to the cart!'
                   }
            return render(request, 'home.html', context)
        else:
            newProToCart = Cart(user_id=u_id,name=pro_name,price=pro_price,quality=pro_quantity)
            newProToCart.save()
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()[:6]
            myCarts = Cart.objects.filter(user_id=current_user_id)
            many_products = Products.objects.all()
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products,
                   'message': 'Add to cart successfully!'
                   }
            return render(request, 'home.html', context)
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()[:6]
        myCarts = Cart.objects.filter(user_id=current_user_id)
        many_products = Products.objects.all()
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products
                   }
        return render(request, 'home.html', context)
    else:
        return redirect(login)
    
def adminProduct(request):
    if request.method == 'POST':
        proName = request.POST.get("name")
        proPrice = request.POST.get("price")
        many_products = Products.objects.all()
        checkExits = Products.objects.filter(name=proName).count()
        if checkExits > 0:
            content = {"message": "Product name already exists",
                       "many_products": many_products}
            return render(request, "admin-product.html",content)
        else:
            newProduct = Products(name=proName,price=proPrice)
            newProduct.save()
            content = {"message": "Product added successully!",
                       "many_products": many_products}
            return render(request, "admin-product.html", content)
        
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_products = Products.objects.all()
        context = {'current_user':[current_user_name, current_user_email],
                   'many_products': many_products
                   }
        return render(request, 'admin-product.html', context)
    else:
        return redirect(login)
    
def updatePro(request,proId,action):
    if request.method == 'POST':
        nameSth = request.POST.get("proUpdName")
        priceSth = request.POST.get("proUpdPrice")
        many_products = Products.objects.all()
        myProduct = many_products.get(id=proId)
        myProduct.name= nameSth
        myProduct.price = priceSth
        myProduct.save()
        return redirect(adminProduct)
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_products = Products.objects.all()
        proUpd = many_products.filter(id=proId)[0]
        context = {'current_user':[current_user_name, current_user_email],
                   'many_products': many_products,
                   'proUpd': proUpd
                   }
        return render(request, 'admin-product.html', context)
    else:
        return redirect(login)

def deletePro(request,prodId,action): 
    many_products = Products.objects.all()
    myProduct = many_products.get(id=prodId)
    myProduct.delete()
    return redirect(adminProduct)

def adminOrders(request):
    if request.method == 'POST':
        oId = request.POST.get("up_id")
        oPay = request.POST.get("up_pay")
        upOrder = Orders.objects.get(id = oId)
        upOrder.payment_status = oPay
        upOrder.save()
        return redirect(adminOrders)
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_orders = Orders.objects.all()
        context = {'current_user':[current_user_name, current_user_email],
                   'many_orders': many_orders
                   }
        return render(request, 'admin-orders.html', context)
    else:
        return redirect(login)
def deleteOrder(request, ordId):
    deadOrder = Orders.objects.get(id = ordId)
    deadOrder.delete()
    return redirect(adminOrders)
def adminUsers(request):
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_users = Users.objects.all()
        context = {'current_user':[current_user_name, current_user_email],
                   'many_users': many_users
                   }
        return render(request, 'admin-users.html', context)
    else:
        return redirect(login)
    
def deleteUser(request,uId):
    deadUser = Users.objects.get(id=uId)
    deadUser.delete()
    return redirect(adminUsers)
def adminContacts(request):
    if 'admin_name' in request.session:
        current_user_name = request.session['admin_name']
        current_user_email = request.session['admin_email']
        many_messages = Message.objects.all()
        context = {'current_user':[current_user_name, current_user_email],
                   'many_messages': many_messages
                   }
        return render(request, 'admin-contacts.html', context)
    else:
        return redirect(login)   
def deleteContact(request, messId):
    deadMess = Message.objects.get(id=messId)
    deadMess.delete()
    return redirect(adminContacts)

def about(request):
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   }
        return render(request, 'about.html', context)
    else:
        return redirect(login)
def shop(request):
    if request.method == 'POST':
        pro_name = request.POST.get("pro_name")
        pro_price = request.POST.get("pro_price")
        pro_quantity = request.POST.get("pro_quantity")
        u_id = request.session['user_id']
        checkExit = Cart.objects.filter(user_id=u_id,name=pro_name).count()
        if checkExit > 0:
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()
            myCarts = allCarts.filter(user_id=current_user_id)
            many_products = Products.objects.all()
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products,
                   'message': 'Product already add to the cart!'
                   }
            return render(request, 'shop.html', context)
        else:
            newProToCart = Cart(user_id=u_id,name=pro_name,price=pro_price,quality=pro_quantity)
            newProToCart.save()
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()
            myCarts = allCarts.filter(user_id=current_user_id)
            many_products = Products.objects.all()
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products,
                   'message': 'Add to cart successfully!'
                   }
            return render(request, 'shop.html', context)
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        many_products = Products.objects.all()
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'allCarts': allCarts,
                   'many_products': many_products
                   }
        return render(request, 'shop.html', context)
    else:
        return redirect(login)
def contact(request):
    if request.method == 'POST':
        u_name = request.POST.get("name")
        u_email = request.POST.get("email")
        u_num = request.POST.get("numberU")
        u_mess = request.POST.get("message")
        checkExit = Message.objects.filter(name=u_name,number=u_num,email=u_email,message=u_mess).count()
        if checkExit > 0:
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()
            myCarts = allCarts.filter(user_id=current_user_id)
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'message': 'Message already sent!'
                   }
            return render(request, 'contact.html', context)
        else:
            newMessage = Message(user_id=request.session['user_id'],name=u_name,number=u_num,email=u_email,message=u_mess)
            newMessage.save()
            current_user_name = request.session['user_name']
            current_user_email = request.session['user_email']
            current_user_id = request.session['user_id']
            allCarts = Cart.objects.all()
            myCarts = allCarts.filter(user_id=current_user_id)
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'message': 'Message sent successfully!'
                   }
            return render(request, 'contact.html', context)

    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   }
        return render(request, 'contact.html', context)
    else:
        return redirect(login)
    
def cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get("cart_id")
        cart_quantity = request.POST.get("cart_quantity")
        newCart = Cart.objects.get(id=cart_id)
        newCart.quality = cart_quantity
        newCart.save()
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        if myCarts.count:
            grandTotal = sum([item.price * item.quality for item in myCarts])
        else:
            grandTotal = 0
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'message': 'Update product successfully!',
                   'grandTotal': grandTotal
                   }
        return render(request, 'cart.html', context)
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        if myCarts.count:
            grandTotal = sum([item.price * item.quality for item in myCarts])
        else:
            grandTotal = 0
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'grandTotal': grandTotal
                   }
        return render(request, 'cart.html', context)
    else:
        return redirect(login)
def deleteCart(request,cId):
    deadCart = Cart.objects.get(id=cId)
    deadCart.delete()
    return redirect(cart)
def deleteAllCart(request,myId,action):
    deadCarts = Cart.objects.filter(user_id=myId).delete()
    return redirect(cart)
def checkout(request):
    if request.method == 'POST':
        nameO = request.POST.get("name")
        numberO = request.POST.get("number")
        emailO = request.POST.get("email")
        addressO = request.POST.get("address")
        nameO = request.POST.get("name")
        methodO = request.POST.get("pay_method")
        placed_onO = date.today().strftime("%Y-%m-%d")
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        if myCarts.count:
            grandTotal = sum([item.price * item.quality for item in myCarts])
        else:
            grandTotal = 0
        total_productO = ''
        for i in range(0,myCarts.count()):
            total_productO += myCarts[i].name + ' (' + str(myCarts[i].quality)+ ')'
            if i != myCarts.count() - 1:
                total_productO += ', '
        checkO = Orders.objects.filter(name=nameO,number=numberO,email=emailO,method=methodO,address=addressO,total_products=total_productO,total_price=grandTotal).count()
        if grandTotal == 0:
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'grandTotal': grandTotal,
                   'message': 'This cart is empty'
                   }
            return render(request,"checkout.html",context)
        elif checkO > 0:
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'grandTotal': grandTotal,
                   'message': 'This order already exists'
                   }
            return render(request,"checkout.html",context)
        else:
            newO = Orders(user_id=current_user_id,name=nameO,number=numberO,email=emailO,method=methodO,address=addressO,total_products=total_productO,total_price=grandTotal,placed_on=placed_onO,payment_status="pending")
            newO.save()
            Cart.objects.filter(user_id=current_user_id).delete()
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': Cart.objects.filter(user_id=current_user_id),
                   'grandTotal': grandTotal,
                   'message': 'Add orders successfully'
                   }
            return render(request,"checkout.html",context)

    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        if myCarts.count:
            grandTotal = sum([item.price * item.quality for item in myCarts])
        else:
            grandTotal = 0
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'grandTotal': grandTotal
                   }
        return render(request, 'checkout.html', context)
    else:
        return redirect(login)
def orders(request):
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        myOrders = Orders.objects.filter(user_id=current_user_id)
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'myOrders': myOrders
                   }
        return render(request, 'orders.html', context)
    else:
        return redirect(login)
def search(request):
    searchStatus = False
    if request.method == 'POST':
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        print(request.POST)
        if 'nameS' in request.POST:
            searchStatus = True
            nameS = request.POST['nameS']
            proRes = Products.objects.filter(name__exact=nameS)
            context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'searchStatus': searchStatus,
                   'proRes': proRes
                   }
            return render(request, 'search_page.html', context)
        else:
            pro_name = request.POST.get("pro_name")
            pro_price = request.POST.get("pro_price")
            pro_quantity = request.POST.get("pro_quantity")
            u_id = request.session['user_id']
            checkExit = Cart.objects.filter(user_id=u_id,name=pro_name).count()
            if checkExit > 0:
                context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'message': 'Product already add to the cart!',
                   'searchStatus': False
                   }
                return render(request, 'search_page.html', context)
            else:
                newProToCart = Cart(user_id=u_id,name=pro_name,price=pro_price,quality=pro_quantity)
                newProToCart.save()
                context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': Cart.objects.filter(user_id=current_user_id),
                   'message': 'Add to cart successfully!',
                   'searchStatus': False
                   }
                return render(request, 'search_page.html', context)      
    if 'user_name' in request.session:
        current_user_name = request.session['user_name']
        current_user_email = request.session['user_email']
        current_user_id = request.session['user_id']
        allCarts = Cart.objects.all()
        myCarts = allCarts.filter(user_id=current_user_id)
        context = {'current_user':[current_user_name, current_user_email, current_user_id],
                   'myCarts': myCarts,
                   'searchStatus': searchStatus
                   }
        return render(request, 'search_page.html', context)
    else:
        return redirect(login)