from django.urls import path
from . import views

urlpatterns = [
    # URL pattern to view journalist
    path('journalist/<int:pk>/', views.journalist_detail, name='journalist_detail'),

    # URL Pattern to subscribe to journalist
    path('<int:pk>/subscribe/', views.subscribe_to_journalist, name='subscribe_to_journalist'),

    # URL Pattern to unsubscribe to journalist
    path('<int:pk>/unsubscribe/', views.unsubscribe_from_journalist, name='unsubscribe_from_journalist'),

    # URL pattern to register account
    path('register/', views.register_user, name='register_user'),

    # URL pattern to login
    path('login/', views.login_user, name='login_user'),

    # URL pattern to logout
    path('login/', views.logout_user, name='logout_user')
]
