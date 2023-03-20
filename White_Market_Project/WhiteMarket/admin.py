from django.contrib import admin
from WhiteMarket.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.register(UserProfile)
admin.register(Sellers)
admin.register(Items)
admin.register(Bids)
admin.register(Stores)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsersInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Sellers)
admin.site.register(Items)
admin.site.register(UserProfile)
admin.site.register(Bids)
admin.site.register(Stores)
