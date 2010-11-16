from django import forms
from models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        exclude = ('cart',)