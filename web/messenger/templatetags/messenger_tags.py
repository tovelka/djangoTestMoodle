from django import template
from messenger.models import Chats, Posts
from django.shortcuts import get_list_or_404


register = template.Library()


@register.inclusion_tag('messenger/includes/get_chats_list.html', name='get_chats')
def get_chats_list():
    chats = get_list_or_404(Chats)
    return {'chats': chats}


# @register.inclusion_tag('messenger/includes/get_cats_list.html', name='get_cats')
# def get_cats_posts():
#     cats = get_list_or_404(Posts.published)
#     return {'cats': cats}


@register.inclusion_tag('messenger/includes/get_posts.html', name='get_posts')
def get_posts_list(category_slug=None):
    if category_slug:
        posts = get_list_or_404(Posts.published, category__slug=category_slug)
    else:
        posts = get_list_or_404(Posts.published)
    return {'posts': posts}