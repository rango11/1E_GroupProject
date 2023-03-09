from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Users,Items,Sellers,Bids,Stores
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime
from django.urls import reverse

def index(request):
    context_dict = {}

    return render(request, 'rango/index.html', context=context_dict)

def showUser(request, user_name_slug):
    context_dict = {}
    try:
        user = Users.objects.get(slug=user_name_slug)
        context_dict['user'] = user
    except Users.DoesNotExist:
        context_dict['user'] = None
    return render(request, 'rango/user.html', context=context_dict)

def showListing(request, item_name_slug):
    context_dict = {}
    try:
        item = Items.objects.get(slug=item_name_slug)
        context_dict['item'] = item
    except Items.DoesNotExist:
        context_dict['item'] = None
    return render(request, 'rango/item.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UsersForm(request.POST)

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
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

@login_required #FIX THIS
def myAccount(request,user_name_slug):
    context_dict = {}

    context_dict['user'] = Users.objects.get(slug=user_name_slug)

    return render(request, 'rango/user.html', context=context_dict)

def listings(request,store_name_slug):
    context_dict = {}
    try:
        item = Stores.objects.get(slug=item_name_slug)
        context_dict['store'] = store
    except Stores.DoesNotExist:
        context_dict['store'] = None

    return render(request, 'rango/listings.html', context=context_dict)


@login_required
def listItem(request):
    form = itemForm()

    if request.method == 'POST':
        form = itemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)

            return redirect(reverse('rango:showListing', kwargs={'itemName': item.name}))
        else:
            print(form.errors)

    return render(request, 'rango/listItem.html', {'form': form})

def terms(request):
    context_dict = {}
    return render(request,'rango/terms.html',context = context_dict)

def contact(request):
    context_dict = {}
    return render(request,'rango/contact.html',context = context_dict)

def about(request):
    context_dict = {}
    return render(request,'rango/about.html',context = context_dict)

def privacy(request):
    context_dict = {}
    return render(request,'rango/privacy.html',context = context_dict)

def checkout(request,item_name_slug):
    context_dict = {}

    context_dict['item'] = Items.objects.get(slug=item_name_slug)
    return render(request,'rango/checkout.html',context_dict)

def transaction(request):
    return render(request,'rango/transaction.html')

def transactionComplete(request):
    return render(request,'rango/transactionComplete.html')
