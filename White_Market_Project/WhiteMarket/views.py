from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from WhiteMarket.models import UserProfile, Items, Sellers, Bids, Stores
from WhiteMarket.forms import *
from datetime import datetime
from django.urls import reverse


def index(request):
    context_dict = {}

    return render(request, 'whitemarketindex.html', context=context_dict)


def showUser(request, user_name_slug):
    context_dict = {}
    try:
        user = UserProfile.objects.get(slug=user_name_slug)
        context_dict['user'] = user
    except UserProfile.DoesNotExist:
        context_dict['user'] = None
    return render(request, 'whitemarketuser.html', context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'whitemarket/register.html', context={'user_form': user_form, 'profile_form': profile_form,
                                                                 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('whitemarket:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'whitemarketlogin.html')


@login_required
def restricted(request):
    return render(request, 'whitemarketrestricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('whitemarket:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


@login_required  # FIX THIS add cookies
def myAccount(request, user_name):
    context_dict = {}

    context_dict['user'] = UserProfile.objects.get(user_name)

    return render(request, 'whitemarket_user.html', context=context_dict)


# def listings(request, itemID):
#     context_dict = {}
#     try:
#         item = Stores.objects.get(itemID)
#         context_dict['store'] = store
#     except Stores.DoesNotExist:
#         context_dict['store'] = None
#
#     return render(request, 'whitemarketlistings.html', context=context_dict)


@login_required
def list_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.userID = request.user
            item.save()

            url = reverse('show_listing', kwargs={'itemID': item.itemID})

            return redirect(url)
    else:
        form = ItemForm()
    return render(request, 'list_item.html', {'form': form})


def show_listing(request, itemID):
    context_dict = {}
    try:
        item = Items.objects.get(itemID)
        context_dict['item'] = item
    except Items.DoesNotExist:
        context_dict['item'] = None
    return render(request, 'whitemarket_item.html', context=context_dict)


def terms(request):
    context_dict = {}
    return render(request, 'whitemarketterms.html', context=context_dict)


def contact(request):
    context_dict = {}
    return render(request, 'whitemarketcontact.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'whitemarketabout.html', context=context_dict)


def privacy(request):
    context_dict = {}
    return render(request, 'whitemarketprivacy.html', context=context_dict)


def checkout(request, item_name_slug):
    context_dict = {}  # User makes this

    context_dict['item'] = Items.objects.get(slug=item_name_slug)
    return render(request, 'whitemarketcheckout.html', context_dict)


def transaction(request, item_name_slug, ):
    # Make the bid
    context_dict = {}
    context_dict["item"] = [item_name_slug]
    return render(request, 'whitemarkettransaction.html')


def transactionComplete(request, item_name_slug, bid_name_slug):
    # Complete the trade and adds the bid info to item, seller Rating
    context_dict = {}
    item = Items.objects.get(slug=item_name_slug)
    bidRecords = Bids.objects.get(item.itemID)

    # context_dict["item"] =
    return render(request, 'whitemarkettransactionComplete.html', context_dict)
