from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DailyTransaction)
admin.site.register(IncrementalUser)
admin.site.register(TotalUser)