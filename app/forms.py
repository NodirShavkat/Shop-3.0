from django import forms
from .models import Product, Order, Comment

# forms.Form
# forms.ModelForm



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
   


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude =('product',)
