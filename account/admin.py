from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

#admin.site.register(Account)
#@admin.register(Account)
#class UniversalAdmin(admin.ModelAdmin):
#    def get_list_display(self, request):
#        return [field.name for field in self.model._meta.concrete_fields]

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin) 
