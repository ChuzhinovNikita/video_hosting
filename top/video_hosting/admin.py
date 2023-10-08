from django.contrib import admin
from .models import *


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Video, SlugAdmin)
admin.site.register(HostingСhannel, SlugAdmin)
admin.site.register(History)
admin.site.register(ViewingQueue)
admin.site.register(Comment)
admin.site.register(CommentParent)
admin.site.register(ComplaintAboutThePost)
