from django.contrib import admin
from .models import UserPreference, SharePreference, GetPreference
# Register your models here. 
admin.site.register(UserPreference)
admin.site.register(SharePreference)
admin.site.register(GetPreference)