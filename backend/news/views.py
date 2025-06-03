from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

from .models import CustomUser, Article, UserPreference, Category
from .forms import RegisterForm_News, RegisterForm_Personal
from .services import get_user_feed

# Create your views here.

def index(request):
    return render(request, 'landing.html')

def register1(request):
    if request.method == "POST":
        form = RegisterForm_Personal(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data.pop('password2', None)
            request.session['registration_data'] = cleaned_data
            print("Session data set:", request.session.get('registration_data'))
            return redirect('register2')
        else:
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm_Personal()
        print("GET request to register1, session data:", request.session.get('registration_data'))
    
    return render(request, 'register.html', {'registerform': form})

def register2(request):
    # Check if user has completed first step
    registration_data = request.session.get('registration_data')
    if not registration_data:
        return redirect('register1')
    
    if request.method == 'POST':
        form = RegisterForm_News(request.POST)
        if form.is_valid():
            # Get personal data from session
            personal_data = registration_data
            
            # Create user with personal data
            user = CustomUser.objects.create_user(
                email=personal_data['email'],
                password=personal_data['password1'],
                first_name=personal_data['first_name'],
                last_name=personal_data['last_name']
            )
            
            # Set additional fields from form
            user.frequency = form.cleaned_data['frequency']
            user.preferred_time = form.cleaned_data['preferred_time']
            user.is_subscribed = form.cleaned_data['is_subscribed']
            
            # Add interests
            interests = form.cleaned_data.get('interests', [])
            if interests:
                user.interests.set(interests)
            else:
                # Set default interests if none selected
                default_interests = Category.objects.filter(name__in=['Technology', 'Business', 'Science'])
                user.interests.set(default_interests)
            
            user.save()
            
            # Clear session data
            request.session.pop('registration_data', None)
            
            # Log the user in
            login(request, user)
            
            # Send welcome email
            try:
                print(f"Attempting to send welcome email to {user.email}")
                send_welcome_email(user)
            except Exception as e:
                print(f"Error sending welcome email: {str(e)}")
            
            return redirect('home')
        else:
            print("Form errors in register2:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm_News()
        print("GET request to register2, session data:", request.session.get('registration_data'))
    
    # Get all categories for the form
    categories = Category.objects.all()
    return render(request, 'register2.html', {'newsform': form, 'categories': categories})

from django.core.management import call_command

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Remove the immediate fetch_articles call
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def home(request):
    # Get filter parameters
    selected_category = request.GET.get('category', '').lower()
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    # Base query for articles
    articles = Article.objects.all().order_by('-created_at')
    
    # Apply category filter
    if selected_category:
        articles = articles.filter(category__name__iexact=selected_category)
    
    # Apply search filter
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    articles_page = paginator.get_page(page)
    
    # Get user's interests for personalization
    user_interests = request.user.interests.all()
    
    # Analyze sentiment and reading level for each article
    from .services import analyze_sentiment, analyze_reading_level
    for article in articles_page:
        article.sentiment_score = analyze_sentiment(article.content) or 0
        article.reading_level = analyze_reading_level(article.content) or 0
    
    context = {
        'articles': articles_page,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'page_obj': articles_page,
        'user_interests': user_interests,
    }
    return render(request, 'home.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    from .services import analyze_sentiment, analyze_reading_level
    sentiment_score = analyze_sentiment(article.content) or 0
    reading_level = analyze_reading_level(article.content) or 0
    
    return render(request, 'article_detail.html', {
        'article': article,
        'generated_summary': '',
        'sentiment_score': sentiment_score,
        'reading_level': reading_level,
    })

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

@login_required
def load_more_articles(request):
    page = request.GET.get('page', 1)
    toggle = request.GET.get('toggle', 'breaking')
    
    try:
        page = int(page)
    except ValueError:
        page = 1
        
    feed = get_user_feed(request.user, toggle)
    paginator = Paginator(feed, 10)  # Show 10 articles per page
    
    try:
        articles = paginator.page(page)
    except:
        return JsonResponse({'error': 'No more articles'}, status=404)
        
    articles_data = [{
        'title': article.title,
        'summary': article.summary,
        'source': article.source,
        'url': article.url,
        'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for article in articles]
    
    return JsonResponse({
        'articles': articles_data,
        'has_next': articles.has_next(),
        'next_page': page + 1 if articles.has_next() else None
    })

@login_required
def send_email(request):
    if request.method == 'POST':
        user = request.user
        subject = 'Welcome to Newsly.AI!'
        message = f'''Hello {user.first_name},

Thank you for using Newsly.AI! This is a test email to confirm that your email settings are working correctly.

Your news preferences:
- Frequency: {user.frequency}
- Preferred Time: {user.preferred_time}
- Interests: {', '.join(interest.name for interest in user.interests.all())}

Best regards,
The Newsly.AI Team'''
        
        try:
            # First, test the connection
            connection = get_connection()
            connection.open()
            
            # If connection is successful, send the email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                connection=connection
            )
            connection.close()
            messages.success(request, 'Test email sent successfully!')
        except Exception as e:
            error_message = str(e)
            if 'timed out' in error_message.lower():
                messages.error(request, 'Connection to email server timed out. Please check your internet connection and try again.')
            elif 'authentication' in error_message.lower():
                messages.error(request, 'Email authentication failed. Please check your email settings.')
            elif 'ssl' in error_message.lower():
                messages.error(request, 'SSL/TLS connection failed. Please check your email settings.')
            else:
                messages.error(request, f'Failed to send email: {error_message}')
            
    return redirect('home')

def send_news_digest_email(user, articles):
    subject = 'Your Newsly Digest is Here 📰'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # Render the HTML content
    html_content = render_to_string('newsDigest.html', {
        'user': user,
        'articles': articles,
    })

    # Send as multipart email
    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@require_http_methods(["POST"])
def send_test_email(request):
    try:
        # Get recipient email from form
        recipient_email = request.POST.get('email', '')
        
        # Create the message
        message = MIMEMultipart()
        message["From"] = settings.EMAIL_HOST_USER
        message["To"] = recipient_email
        message["Subject"] = "Test Email from Newsly.AI"

        # Body of the email
        body = "Hello! This is a test email from Newsly.AI using Gmail's SMTP server."
        message.attach(MIMEText(body, "plain"))

        # Send email using SSL
        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        text = message.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, recipient_email, text)
        server.quit()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test email sent successfully!'
        })
    except Exception as e:
        error_message = str(e)
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to send email: {error_message}'
        }, status=500)

def test_email_page(request):
    return render(request, 'test_email.html')

@login_required
@require_http_methods(["POST"])
def test_email_digest(request):
    """Test endpoint to manually trigger email digests"""
    try:
        digest_type = request.POST.get('digest_type', 'daily')
        if digest_type not in ['daily', 'weekly']:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid digest type. Must be "daily" or "weekly"'
            }, status=400)
            
        # Call the management command
        call_command('send_digests', type=digest_type)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Email digest sent successfully'
        })
        
    except CommandError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error sending digest: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }, status=500)

@login_required
def test_digest_page(request):
    """Render the test email digest page"""
    return render(request, 'test_digest.html')

@login_required
def update_preferences(request):
    if request.method == 'POST':
        user = request.user
        frequency = request.POST.get('frequency', 'daily')
        category_ids = request.POST.getlist('categories')
        
        # Get or create user preferences
        preferences, created = UserPreference.objects.get_or_create(user=user)
        
        # Update frequency
        preferences.frequency = frequency
        
        # Update categories
        preferences.categories.clear()
        preferences.categories.add(*category_ids)
        
        preferences.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def about(request):
    return render(request, 'about.html')

def privacy(request):
    context = {
        'current_year': datetime.datetime.now().year
    }
    return render(request, 'privacy.html', context)

@login_required
def profile(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            request.user.name = name
            request.user.save()
            messages.success(request, 'Profile updated successfully')
    return redirect('profile')

@login_required
def update_preferences(request):
    if request.method == 'POST':
        frequency = request.POST.get('frequency')
        preferred_time = request.POST.get('preferred_time')
        interests = request.POST.getlist('interests')

        if frequency:
            request.user.frequency = frequency
        if preferred_time:
            request.user.preferred_time = preferred_time
        if interests:
            request.user.interests.set(interests)

        request.user.save()
        messages.success(request, 'Preferences updated successfully')
    return redirect('profile')

@login_required
def update_notifications(request):
    if request.method == 'POST':
        is_subscribed = request.POST.get('is_subscribed') == 'on'
        email_notifications = request.POST.get('email_notifications') == 'on'

        request.user.is_subscribed = is_subscribed
        request.user.email_notifications = email_notifications
        request.user.save()

        messages.success(request, 'Notification settings updated successfully')
    return redirect('profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted')
        return redirect('login')
    return redirect('profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect')
            return redirect('profile')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return redirect('profile')
        
        # Update password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Password changed successfully')
        return redirect('profile')
    
    return render(request, 'change_password.html')

    