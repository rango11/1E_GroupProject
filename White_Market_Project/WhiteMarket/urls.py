from django.urls import path
from WhiteMarket import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView


app_name = 'whitemarket'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', TemplateView.as_view(template_name='WhiteMarket/index.html'), name='index'),
    path('about/', views.about, name='about'),
    #path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    #path('add_category/', views.add_category, name='add_category'),
    #path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('listItem/', views.list_item, name='listItem'),
    path('listings/store/<slug:store_name_slug>/', views.store, name='store'),
    path('listings/<slug:item_name_slug>/', views.show_listing, name='showListing'),
    path('user/<slug:username>/', views.showUser, name='showUser'),
    path('checkout/<slug:item_name_slug>/', views.checkout, name='checkout'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactionComplete/<slug:item_name_slug>/<int:bidID>>/', views.transactionComplete, name='transactionComplete'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('createSeller/', views.create_seller, name='createSeller'),


    # path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    # path('register/', views.register, name='register'),
    # path('createSeller/', views.create_seller, name='createSeller'),
    # path('login/', views.user_login, name='login'),
    # path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
    # path('listItem/', views.list_item, name='listItem'),
    # path('myAccount/', views.myAccount, name='myAccount'),
    # path('listings/store/<slug:store_name_slug>/', views.store, name='store'),
    # path('listings/<slug:item_name_slug>/', views.show_listing, name='showListing'),
    # path('user/<slug:username>/', views.showUser, name='showUser'),
    # path('checkout/<slug:item_name_slug>/', views.checkout, name='checkout'),
    # path('transactions/', views.transactions, name='transactions'),
    # path('transactionComplete/<slug:item_name_slug>/<int:bidID>>/', views.transactionComplete, name='transactionComplete'),
    # path('terms/', views.terms, name='terms'),
    # path('contact/', views.contact, name='contact'),
    # path('privacy/', views.privacy, name='privacy'),

]

