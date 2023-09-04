from django.contrib import admin
from .models import *


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Video, SlugAdmin)
