from django.urls import path
from . import views

urlpatterns = [
    # URL pattern to see all articles
    path('', views.view_articles, name='view_articles'),

    # URL pattern to create a new article
    path('create/', views.create_article, name='create_article'),

    # URL pattern to update an article
    path('update/<int:pk>/', views.update_article, name='update_article'),

    # URL pattern to delete an article
    path('delete/<int:pk>/', views.delete_article, name="delete_article"),

    # URL pattern to see all newsletters
    path('newsletters/', views.view_newsletters, name='view_newsletters'),

    # Url pattern to create newsletters
    path('newsletters/create/', views.create_newsletter, name='create_newsletter'),

    # URL pattern to update newsletters
    path('newsletters/update/<int:pk>/', views.update_newsletter, name='update_newsletter'),

    # URL pattern to delete newsletters
    path('newsletters/delete/<int:pk>/', views.delete_newsletter, name='delete_newsletter'),

    # URL to view pending articles (editor)
    path('editor/view/', views.editor_view, name='editor_view'),

    # URL to approve articles
    path('editor/approve/<int:pk>/', views.approve_article, name='approve_article'),

    # URL Patterns publisher endpoint (API)
    path('api/publishers/', views.list_publisher_api, name='list_publisher_api'),
    path('api/publishers/<int:pk>/', views.get_publisher_api, name='get_publisher_api'),
    path('api/publishers/create/', views.create_publisher_api, name='create_publisher_api'),

    # URL patterns Article endpoints (API)
    path('api/articles/', views.list_articles_api, name='list_articles_api'),
    path('api/articles/create/', views.create_article_api, name='create_article_api'),

    # URL patterns Newsletter endpoints (API)
    path('api/newsletters/', views.list_newsletters_api, name='list_newsletters_api'),
    path('api/newsletters/create/', views.create_newsletter_api, name='create_newsletter_api')
]
