"""
URL configuration for shopcart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('customer-signup/',views.customer_signup,name='customer-signup'),
    path('customer-signin/',views.customer_signin,name='customer-signin'),
    path('customer-signout/',views.customer_signout,name='customer-signout'),
    path('customer-profile/<int:id>/',views.customer_profile,name='customer-profile'),
    path('become-seller/',views.become_seller,name='become-seller'),
    path('seller-signup/',views.seller_signup,name='seller-signup'),
    path('seller-signin/',views.seller_signin,name='seller-signin'),
    path('seller-signout/',views.seller_signout,name='seller-signout'),
    path('product-details/<int:id>',views.product_details,name='product-details'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('update-quantity/<int:id>/',views.update_quantity,name='update-quantity'),
    path('remove-cart/<int:id>/',views.remove_cart,name='remove-cart'),
    path('address/',views.address,name='address'),
    
    path('edit-address/<int:id>/',views.edit_address,name='edit-address'),
    path('remove-address/<int:id>/',views.remove_address,name='remove-address'),
    path('confirm-order/<int:id>/',views.confirm_order,name='confirm-order'),
    path('payment/<int:id>/',views.payment,name='payment'),
    path('payment/<int:id>/payment-success/',views.payment_success,name='payment-success'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('reset-password/<int:user_id>/',views.reset_password,name='reset-password')

   
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
