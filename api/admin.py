from django.contrib import admin

from .models import *



admin.site.register(Category)
admin.site.register(Employee)
class BookingAdmin(admin.ModelAdmin):
    list_display=('id','user_id','category')
admin.site.register(Bookingreq)
admin.site.register(workupdate)
admin.site.register(Userregister)
admin.site.register(Login)
admin.site.register(File)


