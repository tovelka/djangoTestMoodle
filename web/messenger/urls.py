from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/<slug:name>/', views.profile, name='profile'),
    path('chats/', views.chats, name='chats'),
    path('chat/<int:chat_id>', views.chat, name='chat'),
    # path('feed/<slug: cat_slug>', views.feed, name='feed_cat'),
    path('feed/<slug:cat_slug>', views.feed, name='feed'),
    path('feed/', views.feed, name='feed'),
    path('post/<slug:post_slug>', views.post, name='post'),
    path('photo/index/', views.photoindex, name='photoindex'),
]