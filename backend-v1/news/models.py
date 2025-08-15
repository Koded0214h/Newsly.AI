from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from datetime import time

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    interests = models.ManyToManyField('Category', related_name='interested_users', blank=True)
    frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='daily')
    preferred_time = models.TimeField(default=time(8, 0))
    is_subscribed = models.BooleanField(default=True)
    last_digest_sent = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    country = models.CharField(
        max_length=2,
        choices=[
            ('us', 'United States'),
            ('gb', 'United Kingdom'),
            ('ng', 'Nigeria'),
            ('ca', 'Canada'),
            ('au', 'Australia'),
            ('in', 'India'),
            ('za', 'South Africa'),
            ('ke', 'Kenya'),
            ('gh', 'Ghana'),
        ],
        default='us'
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='news_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='news_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        # First, remove all many-to-many relationships
        self.interests.clear()
        self.groups.clear()
        self.user_permissions.clear()
        
        # Then delete the user
        super().delete(*args, **kwargs)

class UserPreference(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    categories = models.ManyToManyField('Category', related_name='preferred_by')
    digest_enabled = models.BooleanField(default=True)
    digest_time = models.TimeField(default=time(8, 0))  # Default to 8 AM
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s preferences"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, blank=True)
    url = models.URLField(unique=True)
    content = models.TextField()
    summary = models.TextField(default='')
    sentiment_score = models.FloatField(null=True, blank=True)
    reading_level = models.FloatField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True)
    is_breaking = models.BooleanField(default=False)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']

