from django.contrib import admin
from rango.models import Users, Stores, Items, Tags, Bids 



#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Page, PageAdmin)
#admin.site.register(UserProfile)
admin.site.register(Users)
admin.site.register(Stores)
admin.site.register(Items)
admin.site.register(Tags)
admin.site.register(Bids)