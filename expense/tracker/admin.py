from django.contrib import admin
from .models import *

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list = ['User_Id', 'Name']

class AdminAccount(admin.ModelAdmin):
    list = ['User_Id', 'Username']

class CategoryAccount(admin.ModelAdmin):
    list = ['cat_id', 'Name']

admin.site.register(User, AdminUser)
admin.site.register(account, AdminAccount)
admin.site.register(category, CategoryAccount)
admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(Bank)
admin.site.register(CustomUser)
