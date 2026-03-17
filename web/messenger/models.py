from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.StatusPub.PUBLISHED)


class Chats(models.Model):
    title = models.CharField(max_length=50)
    is_group = models.BooleanField(default=False)
    creator_id = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    avatar = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return (f'Chat {self.title}:\n'
                f'is_group - {self.is_group}\n'
                f'creator_id: {self.creator_id}.\n'
                f'created at: {self.created_datetime}\n')

    class Meta:
        ordering = ['-created_datetime']


class Posts(models.Model):
    class StatusPub(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубиковано'

    title = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    creator_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(default='Empty content')
    is_published = models.BooleanField(choices=StatusPub.choices, default=StatusPub.DRAFT)
    slug = models.SlugField(max_length=255, db_index=True, blank=True)
    category = models.ManyToManyField('PostCategory', blank=True, related_name='posts')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return (f'{self.title}\n')

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class PostCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('feed', kwargs={'cat_slug': self.slug})


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    group = models.TextField(max_length=10, blank=True)
    moodle_id = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return (f'Profile of {self.user.username}:\n'
                f'group - {self.group}\n'
                f'bio: {self.bio}.')
