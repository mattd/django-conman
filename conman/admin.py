from django.conf import settings
from django.contrib import admin

from conman.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        try:
            js = settings.TINYMCE_JS_FILES
        except AttributeError:
            pass

admin.site.register(Page, PageAdmin)
