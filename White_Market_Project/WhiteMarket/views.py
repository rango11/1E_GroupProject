from django.shortcuts import render
from django.http import HttpResponse
from WhiteMarket.models import Category, Page


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    # category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list 
    context_dict['categories'] = None 


    # Render the response and send it back!
    return render(request, 'whitemarket/index.html', context=context_dict)

def about(request):
    return render(request, 'whitemarket/about.html')

def contact(request):
    return render(request, 'whitemarket/contact.html')

def privacy_and_security(request):
    return render(request, 'whitemarket/privacy-andsecuirty.html')

def register(request):
    return render(request, 'whitemarket/register.html')

def login(request):
    return render(request, 'whitemarket/login.html')

def page_not_found(request):
    return render(request, 'whitemarket/page_not_found.html')

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
        # Go render the response and return it to the client.
    return render(request, 'whitemarket/category.html', context=context_dict)

# def add_category(request):
#     form = CategoryForm()

#     if request.method == 'POST':
#         form = CategoryForm(request.POST)

#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('/whitemarket/')
#         else:
#             print(form.errors)
    
#     return render(request, 'whitemarket/add_category.html', {'form': form})

# def add_page(request, category_name_slug):
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#     except:
#         category = None
    
#     # You cannot add a page to a Category that does not exist... DM
#     if category is None:
#         return redirect('/whitemarket/')

#     form = PageForm()

#     if request.method == 'POST':
#         form = PageForm(request.POST)

#         if form.is_valid():
#             if category:
#                 page = form.save(commit=False)
#                 page.category = category
#                 page.views = 0
#                 page.save()

#                 return redirect(reverse('whitemarket:show_category', kwargs={'category_name_slug': category_name_slug}))
#         else:
#             print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
#     context_dict = {'form': form, 'category': category}
#     return render(request, 'whitemarket/add_page.html', context=context_dict)

