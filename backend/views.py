from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from news.models import Article
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from news.services import get_user_feed
import logging

logger = logging.getLogger(__name__)

def home(request):
    # Get user preferences if user is authenticated
    if request.user.is_authenticated:
        try:
            # Get personalized feed based on user's country and interests
            articles = get_user_feed(request.user)
            logger.info(f"Fetched {articles.count()} personalized articles for {request.user.email}")
        except Exception as e:
            logger.error(f"Error getting personalized feed: {str(e)}")
            articles = Article.objects.none()
    else:
        # For non-authenticated users, show all articles
        articles = Article.objects.all().order_by('-published_at')

    # Pagination
    paginator = Paginator(articles, 9)  # Show 9 articles per page (3x3 grid)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'articles': articles,
    })

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

@require_http_methods(["POST"])
@login_required
def fetch_articles(request):
    try:
        # Your existing fetch_articles logic here
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
@login_required
def recategorize_articles(request):
    try:
        # Your existing recategorize_articles logic here
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 