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
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('listItem/', views.list_item, name='listItem'),
    path('listings/<slug:store_name_slug>', views.listings, name='listings'),
    path('listings/<slug:item_name_slug>', views.show_listing, name='showListing'),
    path('user/<slug:user_name_slug>', views.showUser, name='showUser'),
    path('checkout/', views.checkout, name='checkout'),
    path('transaction/', views.transaction, name='transaction'),
    path('transactionComplete/', views.transactionComplete, name='transactionComplete'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

]
