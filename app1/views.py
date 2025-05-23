from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomerSignUpForm,SellerSignUpForm,AddressForm
from .models import CustomUser,CustomerProfile,SellerProfile,Product,Category,Cart,Address,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def index(req):
    selected_categories = req.GET.getlist('category')
    categories = Category.objects.all()
    sort_order = req.GET.get('sort')
    search = req.GET.get('search')


    if selected_categories:
        products = Product.objects.filter(category__id__in = selected_categories ).distinct()
    else:
        products = Product.objects.all()
        
    if sort_order == 'asc':
        products = products.order_by('price')
    elif sort_order == 'dsc':
        products = products.order_by('-price')
        
    if search:
        products = Product.objects.filter(name__icontains = search)
        


    
    context = {
        'products': products,
        'categories': categories,
        'selected_categories': list(map(int,selected_categories)),
        'sort_order': sort_order
        }
    return render(req, 'index.html',context)

def customer_signup(req):
    if req.method == 'POST':
        form = CustomerSignUpForm(req.POST,req.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']    
            contact = form.cleaned_data['contact']
            confirm_password = form.cleaned_data['confirm_password']
            image = form.cleaned_data['image']
            
            if password != confirm_password:
                messages.error(req,'Password does not match')
                return redirect('customer-signup')
    
            else:
                
                try:
                    
                    user = CustomUser.objects.create_user(username=email,first_name=first_name,last_name=last_name,email=email,contact=contact,is_customer=True)
                    user.save()
                    
                    customer = CustomerProfile(user=user,image=image)
                    customer.save()
                    return redirect(req,'customer-signin')
                except:
                    messages.error(req, 'An error occurred during creating user')
                    return redirect('customer-signup')
                    
                              
    else:
        form = CustomerSignUpForm()
            

    context ={
        'form': form
    }
    
    return render(req, 'customer_signup.html',context)


def customer_signin(req):
    if req.method == 'POST':
        form = AuthenticationForm(req,data = req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')  
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_customer:
                    login(req, user)
                    return redirect('index')
                
                else:
                    messages.error(req, 'You are not registered as a seller.')
                    return redirect('seller-signin')
        else:
            messages.error(req, 'Invalid username or password')
            return redirect('customer-signin')
    else:
        form = AuthenticationForm()
            
    
    context = {
        'form': form
    }
    
    return render(req, 'customer_signin.html',context)


def customer_signout(req):
    logout(req)
    return redirect('index')


def customer_profile(req,id):
    
    return render(req,'customer_profile.html')


#Become Seller
def become_seller(request):
    return render(request,'become_seller.html')

#seller signup
def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST,request.FILES) 
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            business_name = form.cleaned_data['business_name']
            gst_number = form.cleaned_data['gst_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = CustomUser.objects.create_user(username = email,first_name=first_name,last_name = last_name,contact = contact, email=email, password=password,is_seller = True)
                user.save()
                seller = SellerProfile.objects.create(user=user, business_name=business_name, gst_number=gst_number,)
                seller.save()

              
                return redirect('become-seller')
            else:
            
                return redirect('seller-signup')
    else:
        form = SellerSignUpForm()
    context = {
        'form': form
    }
    return render(request, 'seller_signup.html',context)


#seller signin
def seller_signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_seller:   
                    login(request, user)
                    return redirect('become-seller')  
                else:
                    messages.error(request, 'You are not registered as a seller.')
                    return redirect('seller-signin')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('seller-signin')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'seller_signin.html', context)

#seller singout
def seller_signout(request):
    logout(request)
    return redirect('become-seller')



def product_details(req,id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category = product.category.id).exclude(id=product.id)
    context = {
        'product': product,
        'date' : datetime.today().date() + timedelta(5),
        'related_products':related_products
        }
    return render(req, 'product_details.html', context)

def add_to_cart(req,id):
    product = Product.objects.get(id=id)
    try:
        user = CustomUser.objects.get(id=req.user.id)
    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    cart_item,created = Cart.objects.get_or_create(product = product,user=user)
    
    if not created:
        cart_item.quantity+=1
        
    cart_item.save()
    return redirect('index')

def cart(req):
    try:
        user = CustomUser.objects.get(id=req.user.id)
        mycart = Cart.objects.filter(user=user)
        total_amount = 0
        total_items = 0
        
        for cart in mycart:
            total_amount += cart.product.price * cart.quantity
            total_items += cart.quantity
        
        gst = total_amount*3/100
        
    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    context = {
        'mycart' : mycart,
        'total_amount' : total_amount,
        'total_items' : total_items,
        'gst' : gst
    }
    return render(req,'cart.html',context)

def update_quantity(req,id):
    product = Cart.objects.get(product=id,user=req.user.id)
    var = req.GET.get('q')
    
    if var == '0':
        if product.quantity>1:
            product.quantity-=1
        else:
            product.quantity=1
    else:
        product.quantity+=1
    product.save()
    return redirect('cart')


def remove_cart(req,id):
    product = Cart.objects.get(product=id,user=req.user.id)
    product.delete()
    return redirect('cart')
    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddressForm
from .models import Address, CustomerProfile

def address(req):
    if req.method == 'POST':
        
        form = AddressForm(req.POST)
        if form.is_valid():
            address_line = form.cleaned_data['address_line']
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pin_code = form.cleaned_data['pin_code']

            address = Address.objects.create(address_line=address_line,street=street,city=city,state=state,pin_code=pin_code
            )
            
            user_profile = CustomerProfile.objects.get(user=req.user)
            user_profile.address.add(address)
            user_profile.save()
            
            messages.success(req, 'Address added successfully!')
            return redirect('address')
        
       
    else:
        form = AddressForm()

    user_profile = CustomerProfile.objects.get(user=req.user)
    addresses = user_profile.address.all()

    context = {
        'addresses': addresses,
        'address_form': form,
    }
    return render(req, 'address.html', context)


def edit_address(req,id):
    address = Address.objects.get(id=id)
    if req.method == 'POST':
        form = AddressForm(req.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(req, 'Address updated successfully!')
            return redirect('address')
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
        'address': address,
    }
    return render(req, 'edit_address.html', context)

def remove_address(req,id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('address')


    

    
    
def confirm_order(req,id):
    address = Address.objects.get(id=id)
    
    try:
        user = CustomUser.objects.get(id=req.user.id)
        mycart = Cart.objects.filter(user=user)
        total_amount = 0
        total_items = 0
        
        for cart in mycart:
            total_amount += cart.product.price * cart.quantity
            total_items += cart.quantity
        
        gst = total_amount*3/100
        
    except CustomUser.DoesNotExist:
        return redirect('customer-signin')
    
    context = {
        'mycart' : mycart,
        'total_amount' : total_amount,
        'total_items' : total_items,
        'gst' : gst,
        'address':address
    }
    return render(req,'confirm_order.html',context)

import random
import razorpay
def payment(request,id):

    if request.user.is_authenticated:
        try:
            user = CustomUser.objects.get(id = request.user.id)
            user_profile = CustomerProfile.objects.get(user=user)
            mycart = Cart.objects.filter(user=user)
            address = Address.objects.get(id=id)
            total_amount=0
            
            for cart in mycart:
                total_amount+=cart.product.price * cart.quantity

                        
            gst = total_amount * 3 / 100
            order_amount = gst + total_amount
            order_id = random.randrange(1000,9999)

            order = Order.objects.create(order_id = order_id,customer = user_profile,shipping_address = address,order_amount = order_amount)
            order.save()

            for cart in mycart:
                OrderItem.objects.create(order_id = order,product = cart.product,quantity = cart.quantity,unit_price = cart.product.price)

            mycart.delete()
            
            
            client = razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ", "UOrbXQGnsEc2dhB1IFg0zNWZ"))

            data = { "amount": int(order_amount*100), "currency": "INR", "receipt": str(order_id) }
            payment = client.order.create(data=data)
            context = {
                'data':data,
                'payment':payment
            }
        
        except CustomUser.DoesNotExist:
            return redirect('customer-signin')
    return render(request,'payment.html',context)


def payment_success(request, id):
    payment_id = request.GET.get('payment_id', 'N/A')
    order_id = request.GET.get('order_id', 'N/A') 

    order = get_object_or_404(Order, order_id=order_id)

    order.payment_status = 'paid'
    order.save()

    context = {
        'payment_id': payment_id,
        'order_id': order_id
    }
    return render(request, 'payment_success.html', context)

  
  
def generate_otp():
    otp = str(random.randrange(100000,999999))  
    return otp



def forgot_password(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            
            req.session['otp'] = otp
            req.session['request_user'] = user.id 
            
            send_mail(
                'Password Request OTP',
                f"Your OTP for password rest is :{otp}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                
    
            )
            return redirect('verify-otp')
        except CustomUser.DoesNotExist:
            messages.error(req,'Email not Registered')
            
            
    return render(req,'forgot_password.html')


def verify_otp(req):
    if req.method == 'POST':
        otp_entered = req.POST.get('otp')
        otp_stored = req.session['otp']
        
        if otp_entered == otp_stored:
            user_id = req.session['request_user']
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                return redirect('reset-password',user_id=user.id)
            else:
                messages.error(req,'session expire please request for otp again')
        else:
            messages.error(req,'Invalid otp')
            return redirect('verify-otp')
    return render(req,'verify_otp.html') 


from django.contrib.auth.forms import SetPasswordForm
def reset_password(req,user_id):
    user = CustomUser.objects.get(id=user_id)
    
    if req.method == 'POST':
        form = SetPasswordForm(user=user,data=req.POST)
        if form.is_valid():
            form.save()
            
            
            if 'otp' in req.session:
                del req.session['otp']
                
            if 'request_user' in req.session:
                    del req.session['request_user']
            messages.success(req,'Your Password Reset Successfully')
            return redirect('customer-signin')
        
    else:
        form = SetPasswordForm(user=user)
    return render(req,'reset_password.html',{'form':form})
    
    