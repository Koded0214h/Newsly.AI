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
import json

def home(request):
    # Get filter parameters
    topic = request.GET.get('topic', '')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    # Base queryset
    articles = Article.objects.all().order_by('-published_at')
    print(f"Total articles before filtering: {articles.count()}")
    
    # Apply filters
    if topic:
        articles = articles.filter(topic=topic)
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    articles_page = paginator.get_page(page)
    print(f"Articles in current page: {len(articles_page)}")
    
    # Get unique topics for filter
    topics = Article.objects.values_list('topic', flat=True).distinct()
    print(f"Available topics: {list(topics)}")
    
    # Debug: Print first article details if available
    if articles_page:
        first_article = articles_page[0]
        print(f"First article title: {first_article.title}")
        print(f"First article summary: {first_article.summary[:100]}...")
    
    context = {
        'articles': articles_page,
        'topics': topics,
        'current_topic': topic,
        'search_query': search_query,
    }
    return render(request, 'home.html', context)

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