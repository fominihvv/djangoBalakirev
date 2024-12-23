from django import template
from django.db.models import Count, Q

from women.models import Category, TagPost

register = template.Library()




@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts', filter=Q(posts__is_published=True))).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count('womens', filter=Q(womens__is_published=True))).filter(total__gt=0)
    return {'tags': tags}
