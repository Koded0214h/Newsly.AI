from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
# Create your models here.

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

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    # Basic preferences
    country = models.CharField(max_length=2, blank=True)
    interests = models.JSONField(default=list, blank=True)  # store category strings or IDs

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
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
    
class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="preferences")
    theme = models.CharField(max_length=20, default="light")  # e.g., 'light', 'dark'
    language = models.CharField(max_length=20, default="en")
    receive_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email}'s Preferences"


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, blank=True)
    url = models.URLField(unique=True)
    content = models.TextField()
    summary = models.TextField(default="", blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)  # -1 to 1
    reading_level = models.FloatField(null=True, blank=True)  # Flesch-Kincaid, etc.
    published_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True)
    is_breaking = models.BooleanField(default=False)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    categories = models.ManyToManyField(Category, related_name="articles", blank=True)
    topics = models.ManyToManyField(Topic, related_name="articles", blank=True)
    tags = models.JSONField(default=list, blank=True)  # free-form tags

    # Personalization metadata
    trending_score = models.FloatField(default=0)  # For ranking in feed
    source_reliability = models.FloatField(null=True, blank=True)  # 0-1 score

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SavedArticle(models.Model):
    """User bookmarks for later reading"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user.email} saved {self.article.title}"


class ReadHistory(models.Model):
    """Tracks what articles a user has read (for recommendations)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="read_history")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="reads")
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article")
        ordering = ["-read_at"]

    def __str__(self):
        return f"{self.user.email} read {self.article.title}"
