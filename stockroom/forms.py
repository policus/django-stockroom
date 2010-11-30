from django import forms
from models import CartItem

class CartItemForm(forms.Form):
    color = forms.IntegerField(required=False)
    measurement = forms.IntegerField(required=False)
    quantity = forms.IntegerField()
    product = forms.IntegerField()