from django.urls import path
from . import views

urlpatterns = [
    # URL Pattern to view publisher details
    path('<int:pk>/', views.publisher_detail, name='publisher_detail'),

    # URL Pattern to subscribe to publisher
    path('<int:pk>/subscribe/', views.subscribe_to_publisher, name='subscribe_to_publisher'),

    # URL pattern to unsubscribe to publisher
    path('<int:pk>/unsubscribe/', views.unsubscribe_from_publisher, name='unsubscribe_from_publisher'),

    # URL pattern to create a publisher
    path('create_publisher', views.create_publisher, name='create_publisher'),
]
