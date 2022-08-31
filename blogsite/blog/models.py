""" Database Schema with custom managers"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .utils import censor
from django.utils.text import slugify


class PublishedPostManager(models.Manager):
    """Custom manager for published posts

    Args:
        models

    Returns:
        Custom manager with only published posts
    """
    def get_queryset(self):
        """QuerySet to return published posts

        Returns:
            Published posts
        """
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """Post model

    Args:
        models
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    objects = models.Manager()
    published_objects = PublishedPostManager()
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=264, null=True,
                        unique_for_date='published_at')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='blog_posts')
    published_at = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='draft')
    origin = models.CharField(max_length=300, default='origin')

    class Meta:
        """Posts published recently will appear first"""
        ordering = ('-published_at',)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.body = censor(self.body)
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Denote detail template by its slug(URL reversing)

        Returns:
            HTML: detail template denoted by its slug
        """
        return reverse('blog:detail', args=[self.slug])


class ActiveCommentManager(models.Manager):
    """Custom manager for active comments

    Args:
        models

    Returns:
        Custom manager for active comments
    """
    def get_queryset(self):
        """QuerySet to return active comments

        Returns:
            Acttive comments
        """
        return super().get_queryset().filter(active=True)


class Comment(models.Model):
    """Comment model

    Args:
        models

    Raises:
        ValueError
    """
    objects = models.Manager()
    active_objects = ActiveCommentManager()
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    origin = models.CharField(max_length=300, default='origin')

    class Meta:
        """Comments created recently will appear first"""
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment {self.body} by {self.name} on {self.post}'

    def save(self, wait= True, *args, **kwargs):
        """Override saving new comment instance

        Raises:
            ValueError
        """
        self.body = censor(self.body)
        if not wait or not self.is_spam_comment(30):
            super().save(*args, **kwargs)
        else:
            raise ValueError('Wait 30 sec')

    def is_spam_comment(self, spam_time_diff):
        """Detect spamming comment via checking the difference
        between current time and created time for the last comment

        Args:
            spam_time_diff (int): Time limit between writing current comment and last comment

        Returns:
            bool: Whether the comment is spam or not
        """
        # If that is the first comment, then It's not spam
        if not Comment.objects.filter(email=self.email, post=self.post).exists():
            return False
        # Obtain the last created comment by the user
        last_user_comment = Comment.objects.filter(email=self.email, post=self.post).first()
        time_diff = timezone.now() - last_user_comment.created_at
        return time_diff.total_seconds() <= spam_time_diff
