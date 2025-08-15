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
        interests = user.interests or []
        language = getattr(user, "preferred_language", "en")
        country = getattr(user, "preferred_country", None)

        fetcher = NewsFetcher(source="newsdata")

        # --- Fetch Interest-Based News ---
        for interest in interests:
            if country:
                local_articles = fetcher.fetch_articles(
                    query=interest,
                    language=language,
                    country=country
                )
                fetcher.save_articles(local_articles)

            global_interest_articles = fetcher.fetch_articles(
                query=interest,
                language=language,
                country=None
            )
            fetcher.save_articles(global_interest_articles)

        # --- Fetch Global News (not tied to interests) ---
        global_keywords = ["world", "international", "global", "technology", "science", "finance"]
        for keyword in global_keywords:
            global_articles = fetcher.fetch_articles(
                query=keyword,
                language=language,
                country=None
            )
            fetcher.save_articles(global_articles)

        # --- Exclude Read Articles ---
        read_ids = ReadHistory.objects.filter(user=user).values_list("article_id", flat=True)
        base_qs = Article.objects.exclude(id__in=read_ids)

        # --- Interest-Based Articles ---
        interest_qs = base_qs.filter(
            Q(categories__name__in=interests) |
            Q(topics__name__in=interests)
        ).distinct()

        # --- True Global Articles (no interest match) ---
        global_qs = base_qs.filter(
            ~Q(categories__name__in=interests),
            ~Q(topics__name__in=interests)
        )

        # --- Filter by Recent & Trending ---
        one_week_ago = timezone.now() - timedelta(days=7)
        interest_qs = interest_qs.filter(
            published_at__gte=one_week_ago
        ).order_by("-trending_score", "-published_at")

        global_qs = global_qs.filter(
            published_at__gte=one_week_ago
        ).order_by("-trending_score", "-published_at")

        # --- Mix 70% Interest, 30% Global ---
        interest_count = int(0.7 * 20)
        global_count = 20 - interest_count

        interest_articles = list(interest_qs[:interest_count])
        global_articles = list(global_qs[:global_count])

        final_articles = interest_articles + global_articles
        random.shuffle(final_articles)

        return final_articles

