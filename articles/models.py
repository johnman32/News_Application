from django.db import models
from publishers.models import Publisher
from django.contrib.auth.models import User
import secrets


class Article(models.Model):
    """
    Model representing an Article

    Fields:
    - title: Title of the article
    - description: Information about the article
    - date_uploaded: Date when article was published
    - category: what article is categorized under
    - published_by: Who uploaded the article
    - author: Who wrote the article
    - image: Uploaded image
    - status: status of the article (pending/approved)
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
    ]

    title = models.CharField(max_length=250)
    description = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=25)
    published_by = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authored_articles')
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """
    Model representing a Newsletter

    Fields:
    - title: Name of newsletter
    - description: Content of newsletter
    - date_sent: When the newsletter is sent out
    - subscribers: Who is subscribed to newsletter
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_newsletters')
    published_by = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class APIClient(models.Model):
    """
    Model to allows users to connect via API

    Fields:
    -name: Name of user connecting
    -api_key: Random generated unique key
    -created_at: time it was generated
    -is_active: Check if key is active
    """
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=64, unique=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    subscribed_journalists = models.ManyToManyField(
        User,
        limit_choices_to={'groups__name': 'Journalist'},
        related_name='api_subscribers',
        blank=True
    )
    subscribed_publishers = models.ManyToManyField(
        User,
        limit_choices_to={'groups__name': 'Publisher'},
        related_name='api_publisher_subscribers',
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
