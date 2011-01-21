from django import forms
from django.contrib.localflavor.us.forms import USStateField
from models import CartItem

class CartItemForm(forms.Form):
    quantity = forms.IntegerField()
    stock_item = forms.IntegerField()
    
class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    address_1 = forms.CharField(max_length=100)
    address_2 = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=3)
    state = USStateField(required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=24, required=False)