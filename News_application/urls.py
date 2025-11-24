from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Admin site URL
    path("admin/", admin.site.urls),

    # Redirect home page to login
    path('', lambda request: redirect('users/login')),

    # Includes Articles URLS
    path('articles/', include('articles.urls')),

    # Includes Publisher URLS
    path('publishers/', include('publishers.urls')),

    # Includes users URLS
    path('users/', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
