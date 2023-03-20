from django import forms
from django.contrib.auth.models import User
from WhiteMarket.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profilePicture', 'description', 'phoneNo')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('itemName','storeID', 'isDigital', 'itemDescription', 'itemImage', 'condition', 'buyNowPrice')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ('bidPrice',)


class SellerForm(forms.ModelForm):
    class Meta:
        model=Sellers
        fields = ('sellerName',)