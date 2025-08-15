from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreference, Article, SavedArticle, ReadHistory

User = get_user_model()

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ["theme", "language", "receive_notifications"]

class UserSerializer(serializers.ModelSerializer):
    preferences = UserPreferenceSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "country", "interests", "date_joined", "preferences"]
        read_only_fields = ["id", "email", "date_joined", "preferences"]

class RegisterSerializer(serializers.ModelSerializer):
    # keep it simple: email + password + optional names
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "country"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        # ensure a preferences row exists
        UserPreference.objects.get_or_create(user=user)
        return user

    def to_representation(self, instance):
        # return full user after registration
        return UserSerializer(instance).data


class ArticleSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    topics = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "url", "summary", "image_url", "published_at",
            "source", "is_breaking", "categories", "topics", "sentiment_score",
            "reading_level", "trending_score"
        ]


class SavedArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = SavedArticle
        fields = ["id", "article", "saved_at"]


class ReadHistorySerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = ReadHistory
        fields = ["id", "article", "read_at"]