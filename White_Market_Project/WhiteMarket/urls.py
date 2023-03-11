# from django.urls import path
# from WhiteMarket import views
# from django.conf import settings
# from django.conf.urls.static import static

# app_name = 'WhiteMarket'

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('about/', views.about, name='about'),
#     path('category/<slug:category_name_slug>/',
#     views.show_category, name='show_category'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# # + static(settings.ITEM_PHOTO_URL, document_root=settings.ITEM_PHOTO_ROOT) + static(settings.USER_PROFILE_PHOTO_URL, document_root=settings.USER_PROFILE_PHOTO_ROOT)

from django.contrib import admin
from django.urls import path
from django.urls import include
from WhiteMarket import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('whitemarket/', include('whitemarket.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)