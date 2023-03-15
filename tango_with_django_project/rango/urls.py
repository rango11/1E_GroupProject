from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    #path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    #path('add_category/', views.add_category, name='add_category'),
    #path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('listItem/', views.listItem, name='listItem'),
    path('listings/', views.listings, name='listings'),
    path('listings/<slug:item_name_slug>', views.showListing, name='showListing'),
    path('user/<slug:user_name_slug>', views.showUser, name='showUser'),
    path('checkout/', views.checkout, name='checkout'),
    path('transaction/', views.transaction, name='transaction'),
    path('transactionComplete/', views.transactionComplete, name='transactionComplete'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
]