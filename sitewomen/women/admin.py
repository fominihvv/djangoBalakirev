from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import Women, TagPost, Category, Husband


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        return [
            ('married', 'Замужен'),
            ('single', 'Не замужен'),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() in ['married', 'Замужен']:
            return queryset.filter(husband__isnull=False)
        elif self.value() in ['single', 'Не замужен']:
            return queryset.filter(husband__isnull=True)
        return queryset


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'photo', 'post_photo', 'post_photo_size', 'content', 'time_create', 'time_update', 'cat',
              'is_published', 'husband',)
    readonly_fields = ('time_create', 'time_update', 'slug', 'post_photo', 'post_photo_size',)
    list_display = (
        'title', 'slug', 'post_photo', 'post_photo_size', 'time_create', 'time_update', 'cat', 'is_published',
        )
    list_display_links = ('title', 'cat',)
    ordering = ('time_create', 'title',)
    search_fields = ('title', 'content', 'cat__name',)
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft', ]
    list_filter = [MarriedFilter, 'cat__name', 'is_published', ]
    save_on_top = True

    @staticmethod
    @admin.display(description='Фотография')
    def post_photo(women: Women) -> str:
        if women.photo:
            return mark_safe(
                f"<a href='{women.photo.url}'><img src='{women.photo.url}' alt='{women.title}' width='200'></a>")
        return 'Нет фото'

    @staticmethod
    @admin.display(description='Размер фотографии')
    def post_photo_size(women: Women) -> str:
        if women.photo:
            return f'{women.photo.width}x{women.photo.height}'
            # return mark_safe(f"<a href='{women.photo.url}'><img src='{women.photo.url}' alt='{women.title}' width='200'></a>")
        return 'Нет фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'{count} записей опубликованы')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей сняты с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


admin.site.register(TagPost)
admin.site.register(Husband)
