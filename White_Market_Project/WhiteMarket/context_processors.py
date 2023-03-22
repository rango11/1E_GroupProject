from WhiteMarket.models import UserProfile,Items,Sellers,Bids,Stores
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#@login_required
def inSellers(request):
    if request.user.is_anonymous:
        return {'inSeller': False}

    currentUser = UserProfile.objects.get(user=request.user)
    sellerList = Sellers.objects.all()

    for seller in sellerList:
        if currentUser == seller.userID:
            return {'inSeller':True}

    return {'inSeller':False}

def getStores(request):
    stores = Stores.objects.all()
    return {'stores':stores}
