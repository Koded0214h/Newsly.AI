from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.db.models import Q
import random

from datetime import timedelta
from django.utils import timezone

from .services.news_fetcher import (
    NewsFetcher
)

from .serializers import (
    RegisterSerializer, UserSerializer, UserPreferenceSerializer,
    ArticleSerializer
)
from .models import (
    UserPreference, Article, ReadHistory
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # auto-create if missing
        pref, _ = UserPreference.objects.get_or_create(user=self.request.user)
        return pref


class PersonalizedFeedView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        total_count = 20  # Total articles to return
        local_ratio = 0.7  # 70% local content
        
        # Get user preferences
        interests = user.interests.all()
        interest_names = list(interests.values_list('name', flat=True))
        country = user.country if hasattr(user, 'country') else None
        
        # Base queryset - recent articles not read by user
        one_week_ago = timezone.now() - timedelta(days=7)
        read_ids = ReadHistory.objects.filter(user=user).values_list('article_id', flat=True)
        
        base_qs = Article.objects.filter(
            published_at__gte=one_week_ago
        ).exclude(
            id__in=read_ids
        ).distinct()
        
        # --- Local Articles (70%) ---
        local_count = int(total_count * local_ratio)
        
        # Get local articles matching interests
        local_qs = base_qs.filter(
            Q(topics__name__in=interest_names) | Q(categories__name__in=interest_names),
            country=country
        ) if country else Article.objects.none()
        
        local_articles = list(local_qs.order_by('-trending_score', '-published_at')[:local_count])
        
        # If not enough local articles, reduce local count
        actual_local_count = len(local_articles)
        if actual_local_count < local_count:
            local_count = actual_local_count
        
        # --- Global Articles (30%) ---
        global_count = total_count - local_count
        
        # Get global articles in two batches to maintain diversity
        # 1. Global articles matching interests
        global_interest_qs = base_qs.filter(
            Q(topics__name__in=interest_names) | Q(categories__name__in=interest_names)
        )
        if country:
            global_interest_qs = global_interest_qs.exclude(country=country)
        
        # 2. Global articles not matching interests
        global_non_interest_qs = base_qs.filter(
            ~Q(topics__name__in=interest_names),
            ~Q(categories__name__in=interest_names)
        )
        if country:
            global_non_interest_qs = global_non_interest_qs.exclude(country=country)
        
        # Get half from each global category
        half_global = max(1, global_count // 2)
        
        global_interest_articles = list(
            global_interest_qs.order_by('-trending_score', '-published_at')[:half_global]
        )
        global_non_interest_articles = list(
            global_non_interest_qs.order_by('-trending_score', '-published_at')[:global_count - half_global]
        )
        
        global_articles = global_interest_articles + global_non_interest_articles
        
        # --- Combine results ---
        final_articles = local_articles + global_articles
        
        # If we still don't have enough articles, fill with whatever is available
        if len(final_articles) < total_count:
            remaining = total_count - len(final_articles)
            fallback_articles = list(
                base_qs.exclude(id__in=[a.id for a in final_articles])
                .order_by('-trending_score', '-published_at')[:remaining]
            )
            final_articles.extend(fallback_articles)
        
        # Shuffle while keeping local articles mostly first
        random.shuffle(local_articles)
        random.shuffle(global_articles)
        final_articles = local_articles + global_articles
        
        return final_articles