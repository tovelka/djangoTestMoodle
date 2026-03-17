from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse
from messenger.models import Posts, PostCategory
# from django.template.loader import render_to_string
# Create your views here.


menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Лента', 'url_name': 'feed'},
    {'title': 'Профиль', 'url_name': 'profile'},
    {'title': 'Чаты', 'url_name': 'chats'},
]


def index(request):
    data = {'menu': menu, 'title': 'Главная'}
    return render(request, 'messenger/index.html', context=data)


def feed(request, cat_slug=''):
    cats = get_list_or_404(PostCategory.objects.filter(pk__in=Posts.published.values_list('category', flat=True)))
    data = {'menu': menu, 'title': 'Лента', 'cats': cats, 'cat_slug': cat_slug}
    return render(request, 'messenger/feed.html', context=data)


def post(request, post_slug):
    post = get_object_or_404(Posts, slug=post_slug)
    data = {'menu': menu, 'title': post.title, 'post': post}
    return render(request, 'messenger/post.html', context=data)


def profile(request, name):
    data = {'menu': menu, 'title': 'Профиль', 'name': name}
    return render(request, 'messenger/profile.html', context=data)


def chats(request):
    data = {'title': 'Чаты', 'menu': menu}
    return render(request, 'messenger/chats.html', context=data)


def chat(request, chat_id):
    data = {'title': 'Чат', 'chat_id': chat_id}
    return render(request, 'messenger/chat.html', context=data)


def photoindex(request):
    return render(request, 'messenger/photo.html')


def page_404(request, exception):
    uri = reverse('home')
    return redirect(uri)