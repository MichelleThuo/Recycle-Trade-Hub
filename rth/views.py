from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import auth, messages
import uuid, json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from .models import Products, Cart, Order, MpesaPayment
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializer import ProductSerializer, OrderSerializer
from .mpesa import mpesa_pay
from django.views.decorators.csrf import csrf_exempt
from .mails import send_mail_after_order
from chat.models import Profile
from django.db.models import   Sum

def mycontextprocessor(request):
    try:
        profile=Profile.objects.get(user=request.user)
    except:
        profile=None
    context={
        'profile':profile
    }
    return context

def index(request):
    return render(request, 'index.html')
        
def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        name=request.POST['userName']
        email=request.POST['email']
        password=request.POST['password']
        mobile=request.POST['mobile']

        if User.objects.filter(email=email).exists():
            return redirect('/register')
        user=User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        profile=Profile.objects.create(user=user, phone=mobile, bio='')
        profile.save()
        return redirect('/login/')
    else:
        return render(request, 'registerPage.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email=request.POST['email']
            password=request.POST['password']
            user=auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request,user)
            else:
                messages.info(request, "Invalid Login credencials")
            return redirect('/login/')
        else:
            return render(request, 'loginPage.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
     
def inbox(request):
    
    return render(request,'inbox.html')



def search(request):
    tearm=request.GET['q']
    products=Products.objects.filter(productName__icontains=tearm)
    context={
        'products':products,
    }
    response=render(request, 'productList.html', context)
    return response



def cart(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("/login/")
        cookie=request.COOKIES.get('cart')
        cart=Cart.objects.filter(cartcookie=cookie)  
        price_arr=[]
        for c in cart:
            price_arr.append(c.qty*c.product.price)
        
        sum=0
        for s in price_arr:
            sum+=s
        phone=request.POST['phone']
        amount=int(sum) #request.POST['price']
        callback='https://recycletradehub.shahibu.com/mpesa/callback/'
        user_id=request.user.id
        reason='Buy New Goods'
        d=mpesa_pay(phone, amount,callback, user_id, reason)
        data={
             'MerchantRequestID': '6e86-45dd-91ac-fd5d4178ab52861416', 
             'CheckoutRequestID': 'ws_CO_12032024173304297758095711', 
             'ResponseCode': '0', 
             'ResponseDescription': 'Success. Request accepted for processing', 
             'CustomerMessage': 'Success. Request accepted for processing'
             } 
        try:
            for c in cart:
                order=Order.objects.create(merchant_request_id=data['MerchantRequestID'],checkout_request_id=data['CheckoutRequestID'],seller=c.product.seller,buyer=request.user,products=c.product,qty=c.qty,price=c.product.price*c.qty)   
            send_mail_after_order(request.user, cart)
            cart.delete()
            return redirect('/orders/')
        except:
            print("Error")

        return redirect('/cart')
    
    if not request.COOKIES.get('cart'):
        response=redirect('/cart')
        response.set_cookie('cart', uuid.uuid4()) 
        return response
    else: 
        cookie=request.COOKIES.get('cart')
        cart=Cart.objects.filter(cartcookie=cookie)  
        cart_count=cart.count()
        p=[]
        for c in cart:
            price=str(c.product.price*c.qty)
            p.append(price)
        sum=0
        for s in p:
            sum=float(s)+sum
        context={
            'cart_items':cart,
            'cart_count':cart_count,
            'sub_total':sum
        }
        return render(request, 'cart.html', context)


def add_to_cart(request, id, qty):
    if not request.COOKIES.get('cart'):
        response=redirect(f'/addcart/{id}/{qty}/')
        response.set_cookie('cart', uuid.uuid4()) 
    else: 
        id=int(id)
        cookie=request.COOKIES.get('cart')
        product=Products.objects.get(id=id)
        if qty == 'delete':
                c=Cart.objects.filter(cartcookie=cookie, product=product)
                c.delete()
                return HttpResponse(f"deleted {c}")
        try:
            cart, created=Cart.objects.get_or_create(cartcookie=cookie, product=product)
            print("Product:", cart, "Created:", created)
            max_qty=int(Products.objects.get(id=id).qty)
            if not created:
                if int(qty)>=-1 and int(qty)<=max_qty:
                    if qty == '1':
                        try:
                            if cart.qty <= max_qty and cart.qty >=1:
                                cart.qty = cart.qty+1
                            else:
                                cart.qty=max_qty
                        except:
                            cart.qty=1
                    elif qty == '-1':
                        try:
                            if cart.qty <= 1:
                                pass
                            else:
                                cart.qty=cart.qty-1
                        except:
                            cart.qty=0
                    elif qty == '0':
                        c=Cart.objects.filter(cartcookie=cookie, product=product)
                    else:
                        cart.qty=int(qty)
                else:
                    cart.qty=1
                    
                cart.save()
        except Exception as e:
            messages.info(request, "Item not found")
            qty=e
        response=HttpResponse(qty)
    return response


# addtocart/id/qty
# addtocart/1/2
def myprofile_removed(request):
    products=Products.objects.filter(seller=request.user.id)
    page_n=request.GET.get('page',1)
    p=Paginator(products, 1)
    try:
        page=p.page(page_n)
    except EmptyPage:
        page=p.page(1)
    pg_total=p.num_pages
    pgs=[]
    for i in range(1, pg_total+1):
        pgs.append(i)
    context={
        'myproducts':page,
        'page_count':pg_total,
        'ranges':pgs

    }
    return render(request, 'profile.html', context)


class Myproductapi(generics.ListAPIView):
    serializer_class=ProductSerializer
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        id=self.request.user.id
        data=Products.objects.filter(seller=id)
        return data
    
class MySellerOrderapi(generics.ListAPIView):
    serializer_class=OrderSerializer
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        id=self.request.user.id
        data=Order.objects.filter(seller=id) #change to below
        # data=Order.objects.filter(seller=id, order_status='True', payment_status='True')
        # print(data)
        return data
    
class MyOrderapi(generics.ListAPIView):
    serializer_class=OrderSerializer
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        id=self.request.user.id
        data=Order.objects.filter(buyer=id) #Change to below
        # data=Order.objects.filter(buyer=id, order_status='True', payment_status='True')
        # print(data)
        return data

def myprofile(request):
    if not request.user.is_authenticated:
        messages.info(request, "login First to view this page")
        return redirect('/login/')
    user=User.objects.get(id=request.user.id)
    
    if request.method=='POST':
        profile=Profile.objects.get(user=request.user)
        user.save()
        if 'image' in request.FILES:
            image=request.FILES['image']
            profile.image=image
            profile.save()
        return redirect('/my')
    
    return render(request, 'my/my.html')

def myorders(request):
    if not request.user.is_authenticated:
        messages.info(request, "login First to view this page")
        return redirect('/login/')
    total=Order.objects.filter(seller=request.user).aggregate(Sum('price'))['price__sum']
    context={"total":total}
    return render(request, 'my/orders.html', context)

def ordersView(request):
    if not request.user.is_authenticated:
        messages.info(request, "login First to view this page")
        return redirect('/login/')
    return render(request, 'my/orderbyme.html')

def profile1(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login First to view this page")
        return redirect('/login/')
    if request.method=='POST':
        seller=request.user
        productName=request.POST['productName']
        description=request.POST['description']
        price=request.POST['price']
        qty=request.POST['qty']
        for x in request.FILES:
            print("Files",x)
        if 'photo' in request.FILES:
            photo=request.FILES['photo']
            print("Photo available")
            try:
                p=Products.objects.create(seller=seller,productName=productName, photo=photo,description=description,price=price,qty=qty  )
            except:
                pass
        print("Post")
        return redirect('/my/products/')
        
    context={}
    return render(request, 'my/myproducts.html', context)

def updatemyproduct(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login First to view this page")
        return redirect('/login/')
    if request.method=='POST':
        seller=request.user
        pid=request.POST['p_id']
        productName=request.POST['p_name']
        description=request.POST['product_description']
        price=request.POST['product_price']
        qty=request.POST.get('product_qty',1)
        p=Products.objects.get(seller=seller,id=pid)
        if 'photo' in request.FILES:
            photo=request.FILES['photo']
            try:
                p.photo=photo
            except:
                pass
        p.productName=productName
        p.description=description
        p.price=price
        p.qty=qty
        p.save()
    return redirect('/my/products/')


def deletemyproduct(request, number):
    if request.user.is_authenticated:
        product=Products.objects.filter(seller=request.user, id=number)
        product.delete()
        return HttpResponse("Deleted")
    else:
        HttpResponse("Unauthorized")


def myInbox(request):
    if not request.user.is_authenticated:
        messages.info(request, "login First to view this page")
        return redirect('/login/')
    return render(request, 'my/inbox.html')

@csrf_exempt    
def MpesaIPN(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        callback_data = data.get('Body').get('stkCallback')
        metadata_items = callback_data.get('CallbackMetadata').get('Item')
        metadata = {item['Name']: item['Value'] for item in metadata_items}
        merchant_request_id=callback_data.get('MerchantRequestID')
        checkout_request_id=callback_data.get('CheckoutRequestID')
        payment = MpesaPayment.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=callback_data.get('ResultCode', ''),
            result_desc=callback_data.get('ResultDesc', ''),
            amount=metadata.get('Amount', 0),
            mpesa_receipt_number=metadata.get('MpesaReceiptNumber', ''),
            transaction_date=datetime.strptime(str(metadata.get('TransactionDate', '')), "%Y%m%d%H%M%S"),
            phone_number=metadata.get('PhoneNumber', '')
        )
        order=Order.objects.filter(merchant_request_id=merchant_request_id,checkout_request_id=checkout_request_id)       
        order.update(payment_status='True',order_status='True')

    return HttpResponse("Ok")
