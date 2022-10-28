import json
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

class ProductView(View):
    def get(self,request):
        topweares = Product.objects.filter(category='TW')
        buttomweares = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request,'app/home.html',{'topwears':topweares,'bottomwears':buttomweares,'mobile':mobile,'laptop':laptop})

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})


def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        #print(cart)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        #list comprihansion ko use gareko yesma k hunxa bhane si p ma cart ko parteek object haru aaunxaan aani p.user == user le varify garxa user lai aani last ma saab lai p ma assign garxa list banayera yek yek ko
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount = amount + tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app.emptycart.html')



def remove_cart(request):
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
            
            c.delete()
            user = request.user
            amount = 0.0
            shipping_amount = 70.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]

            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount = amount + tempamount
                

        data= {
                
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

        
        

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
    add =Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')



def mobile(request,data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Realme' or data == 'MI' :   
        mobile = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html',{'mobile':mobile})

def laptop(request,data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Dell' or data == 'Acer' or data == 'lenovo':
        laptop = Product.objects.filter(category='L').filter(brand=data)  
    return render(request,'app/laptop.html',{'laptop':laptop})

def topwear(request):
        topwear = Product.objects.filter(category = 'TW')
        return render(request,'app/topweare.html',{'topwear':topwear})

def butomwear(request):
    butomwear=Product.objects.filter(category = 'BW')
    return render(request,'app/buttomwear.html',{'butomwear':butomwear})

def login(request):
 return render(request, 'app/login.html')
 
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount   
        totalamount = amount + shipping_amount 
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request,'Congratulation!! Registered Successfully')
                form.save()
        return render(request,'app/customerregistration.html',{'form':form}) 


class ProfileView(View):
    def get(self,request):
        form = CustumerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form = CustumerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city=form.cleaned_data['city']
            provience=form.cleaned_data['provience']
            zipcode=form.cleaned_data['zipcode']   
            reg = Customer(user=usr,name=name,locality=locality,city=city,provience=provience,zipcode=zipcode) 
            reg.save()
            messages.success(request,'Congratulation Profile Updated')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


