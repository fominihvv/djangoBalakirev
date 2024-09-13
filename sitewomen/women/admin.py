from django.contrib import admin

from .models import Women, TagPost, Category, Husband


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'time_update', 'cat', 'is_published')
    list_display_links = ('title', 'cat')
    ordering = ('time_create', 'title')
    search_fields = ('title', 'content')
    #list_editable = ('is_published',)


# Register your models here.


admin.site.register(TagPost)
admin.site.register(Category)
admin.site.register(Husband)
