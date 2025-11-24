from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Newsletter, APIClient
from .forms import ArticleForm, NewsletterForm
from django.contrib.auth.decorators import permission_required
from .serializers import NewsletterSerializer, ArticleSerializer, PublisherSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from publishers.models import Publisher
from .permission import IsJournalist
from functools import wraps
from django.http import JsonResponse
from django.db import models
from django.contrib import messages


def view_articles(request):
    """
    View to list all articles

    Parameters:
    - request: HTTP request object
    - Returns: Rendered HTML Page with list of articles
    """
    articles = Article.objects.filter(status='approved')
    return render(request, 'articles/view_articles.html', {'articles': articles})


@permission_required('articles.add_article', raise_exception=True)
def create_article(request):
    """
    View to create an article object

    Parameters:
    - request: HTTP request object
    - Returns: Redirects to article list upon success
    """
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("view_articles")

    else:
        form = ArticleForm()
    return render(request, 'articles/create_article.html', {'form': form})


@permission_required('articles.change_article', raise_exception=True)
def update_article(request, pk):
    """View to update article object"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('view_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/update_article.html', {
        'form': form,
        'article': article})


@permission_required('articles.delete_article', raise_exception=True)
def delete_article(request, pk):
    """View to delete article object"""
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        article.delete()
        return redirect("view_articles")


def view_newsletters(request):
    """
    View to list all newsletters

    Parameters:
    - Request: Http Object
    - Return: Rendered html page of newsletters
    """
    newsletters = Newsletter.objects.all()
    return render(request, "articles/view_newsletters.html", {'newsletters': newsletters})


@permission_required('articles.add_newsletter', raise_exception=True)
def create_newsletter(request):
    """
    View to create a newsletter object

    Parameters:
    - request: HTTP request object
    - Returns: Redirects to article list upon success
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("view_newsletters")

    else:
        form = NewsletterForm()
    return render(request, 'articles/create_newsletter.html', {'form': form})


@permission_required('articles.change_newsletter', raise_exception=True)
def update_newsletter(request, pk):
    """
    View to update an existing newsletter
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect("view_newsletters")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'articles/update_newsletter.html', {'form': form, 'newsletter': newsletter})


@permission_required('articles.delete_newsletter', raise_exception=True)
def delete_newsletter(request, pk):
    """
    View to delete a newsletter
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if request.method == "POST":
        newsletter.delete()
        return redirect("view_newsletters")


def editor_view(request):
    """
    View to allow editors to see pending articles
    """
    pending_articles = Article.objects.filter(status='pending')
    return render(request, 'articles/editor_view.html', {'pending_articles': pending_articles})


def approve_article(request, pk):
    """
    View to approve a pending article
    """
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.status = 'approved'
        article.approved_by = request.user
        article.save()

        messages.success(request, f'Article "{article.title}" has been approved!')
        return redirect('editor_view')

    return redirect('editor_view')


def api_key_check(view_func):
    """Check if client has an API KEY"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.GET.get('api_key')

        if not api_key:
            return JsonResponse({
                'error': 'API key required',
            }, status=401)

        try:
            client = APIClient.objects.get(api_key=api_key, is_active=True)
            request.api_client = client
            return view_func(request, *args, **kwargs)
        except APIClient.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid API key',
            }, status=403)

    return wrapper


@api_view(['GET'])
@permission_classes([AllowAny])
def list_publisher_api(request):
    """List all publisher API view"""
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_publisher_api(request, pk):
    """
    Get Publisher by ID (API VIEW)
    """
    try:
        publisher = Publisher.objects.get(pk=pk)
    except Publisher.DoesNotExist:
        return Response({'error': 'Publisher not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PublisherSerializer(publisher)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsJournalist])
def create_publisher_api(request):
    """
    Create a new publisher (API view)
    """
    serializer = PublisherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
@api_key_check
def list_articles_api(request):
    """
    List all articles (API View)
    """
    client = request.api_client
    subscribed_journalists = client.subscribed_journalists.all()
    subscribed_publishers = client.subscribed_publishers.all()

    articles = Article.objects.filter(
        status='approved'
    ).filter(
        models.Q(author__in=subscribed_journalists) |
        models.Q(author__in=subscribed_publishers)
    ).order_by('-date_uploaded')

    serializer = ArticleSerializer(articles, many=True)

    return Response({
        'client': client.name,
        'total_articles': articles.count(),
        'articles': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsJournalist])
def create_article_api(request):
    """
    Create new article (API_view)
    """
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_newsletters_api(request):
    """
    List all Newsletters (Api_view)
    """
    newsletters = Newsletter.objects.all().order_by('-date_sent')
    serializer = NewsletterSerializer(newsletters, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsJournalist])
def create_newsletter_api(request):
    """
    Create newsletter object (API_view)
    """
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
