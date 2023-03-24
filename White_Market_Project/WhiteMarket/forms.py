from django import forms
from WhiteMarket.models import *
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
   
   
    class Meta:
        model = UserProfile
        fields = ('profilePicture', 'description', 'phoneNo')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('itemName', 'storeID', 'isDigital', 'itemDescription', 'itemImage', 'condition', 'buyNowPrice')
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['itemImage'].required = False

class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ('bidPrice',)


class SellerForm(forms.ModelForm):
    class Meta:
        model = Sellers
        fields = ('sellerName',)
