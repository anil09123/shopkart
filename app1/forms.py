from django import forms
from .models import CustomerProfile,SellerProfile,Address

from .models import CustomUser

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    image = forms.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','contact')
        
    
        
class SellerSignUpForm(forms.ModelForm):
    business_name = forms.CharField()
    gst_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email', 'contact')  

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'street', 'city', 'state', 'pin_code']
        