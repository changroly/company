from django.contrib import admin
from qnaapi.models import users

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','buy','created_time','question')
admin.site.register(users, usersAdmin)
