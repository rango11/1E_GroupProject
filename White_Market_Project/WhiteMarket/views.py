from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from WhiteMarket.models import UserProfile, Items, Sellers, Bids, Stores
from WhiteMarket.forms import *
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.views import LogoutView, LoginView
from WhiteMarket.forms import UserForm, UserProfileForm, ItemForm


def index(request):
    context_dict = {}

    return render(request, 'whitemarket/index.html', context=context_dict)


def showUser(request, username):
    context_dict = {}
    try:
        targetUser = User.objects.get(username=username)
        context_dict['user'] = targetUser
        context_dict['userProfile'] = UserProfile.objects.get(user=targetUser)
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['userProfile'] = None
    return render(request, 'whitemarket/user.html', context=context_dict)


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
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'whitemarket/login.html', {'form': form})
    #
    #     if user:
    #         if user.is_active:
    #             login(request, user)
    #             return redirect(reverse('whitemarket:index'))
    #         else:
    #             return HttpResponse("Your whitemarket account is disabled.")
    #     else:
    #         print(f"Invalid login details: {username}, {password}")
    #         return HttpResponse("Invalid login details supplied.")
    # else:
    #     return render(request, 'whitemarket/login.html')


# class CustomLoginView(LoginView):
#     authentication_form = CustomLoginForm
#     template_name = 'whitemarket/login.html'


@login_required
def restricted(request):
    return render(request, 'whitemarket/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('whitemarket:logout'))


class WhiteMarketLogoutView(LogoutView):
    next_page = 'my_custom_logout_page'


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


@login_required
def myAccount(request):
    # url = reverse("whitemarket:showUser", kwargs={'username': request.user.username})
    url = reverse("whitemarket:showUser", kwargs={'username': request.user.username})

    return redirect(url)


def listings(request, store_name_slug):
    context_dict = {}
    try:
        store = Stores.objects.get(slug=store_name_slug)
        context_dict['store'] = store
    except Stores.DoesNotExist:
        context_dict['store'] = None

    return render(request, 'whitemarket/listings.html', context=context_dict)


@login_required
def list_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            seller = Sellers.objects.get(userID=UserProfile.objects.get(user=request.user).userID)
            if seller != None:
                item = form.save(commit=False)
                item.sellerID = seller
                item.sellerName = seller.sellerName
                item.save()

                url = reverse("whitemarket:showListing", kwargs={'item_name_slug': item.slug})

                return redirect(url)
    else:
        form = ItemForm()
    return render(request, 'whitemarket/listItem.html', {'form': form})


@login_required
def create_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.userID = UserProfile.objects.get(user=request.user)
            seller.save()

<<<<<<< HEAD
            # url = reverse('whitemarket:createSeller', kwargs={'userID': seller.userID})

            # return redirect(url)
=======
>>>>>>> feature/functionality
    else:
        form = SellerForm()

    return render(request, 'whitemarket/createSeller.html', {'form': form})


def show_listing(request, item_name_slug):
    context_dict = {}
    try:
        item = Items.objects.get(slug=item_name_slug)
        context_dict['item'] = item
    except Items.DoesNotExist:
        context_dict['item'] = None

    currentUser = UserProfile.objects.get(user=request.user)
    context_dict['currentUser'] = currentUser

    context_dict["bids"] = Bids.objects.filter(itemID=item.itemID)

    try:

        seller = Sellers.objects.get(userID=currentUser)

        if item.sellerID == seller.sellerID:
            context_dict["seller"] = seller
        else:
            context_dict['seller'] = Sellers.objects.get(sellerName=item.sellerName)
    except Sellers.DoesNotExist:
        context_dict['seller'] = Sellers.objects.get(sellerName=item.sellerName)

    return render(request, 'whitemarket/item.html', context=context_dict)


def terms(request):
    context_dict = {}
    return render(request, 'whitemarket/terms.html', context=context_dict)


def contact(request):
    context_dict = {}
    return render(request, 'whitemarket/contact.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'whitemarket/about.html', context=context_dict)


def privacy(request):
    context_dict = {}
    return render(request, 'whitemarket/privacy.html', context=context_dict)


def checkout(request, item_name_slug):
    if request.method == 'POST':
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.itemID = Items.objects.get(slug=item_name_slug)
            bid.userID = UserProfile.objects.get(user=request.user)
            bid.bidTime = datetime.now()
            bid.save()

            if bid.bidPrice == Items.objects.get(slug=item_name_slug).buyNowPrice:
                url = reverse("whitemarket:transactionComplete",
                              kwargs={'item_name_slug': item_name_slug, 'bidID': bid.bidID})
            else:
                url = reverse("whitemarket:showListing", kwargs={'item_name_slug': item_name_slug})

            return redirect(url)
    else:
        form = BidForm()

    return render(request, 'whitemarket/checkout.html', {'form': form, 'itemSlug': item_name_slug})


def transactionComplete(request, item_name_slug, bidID):
    item = Items.objects.get(slug=item_name_slug)
    bid = Bids.objects.get(bidID=bidID)
    bid.complete = True;
    bid.save()

    item.sellTime = datetime.now()
    item.save()

    context_dict = {}
    context_dict["item"] = item
    context_dict["username"] = request.user.username

    return render(request, 'whitemarket/transactionComplete.html', context_dict)


def store(request, store_name_slug):
    context_dict = {}
    try:
        store = Stores.objects.get(slug=store_name_slug)
        context_dict['store'] = store
    except Stores.DoesNotExist:
        store = None
        context_dict['store'] = None

    context_dict['items'] = Items.objects.filter(storeID=store.storeID)

    return render(request, 'whitemarket/store.html', context_dict)


def transactions(request):
    currentUser = UserProfile.objects.get(user=request.user)

    context_dict = {}

    context_dict['completeBids'] = Bids.objects.filter(userID=currentUser.userID, complete=True)
    context_dict['uncompleteBids'] = Bids.objects.filter(userID=currentUser.userID, complete=False)

    return render(request, 'whitemarket/transactions.html', context_dict)
