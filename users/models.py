from django.db import models
from django.contrib.auth.models import User, Group
from articles.models import Publisher, Article, Newsletter


class UserProfile(models.Model):
    """
    Model representing a user

    Fields:
    - ROLE_CHOICES: differentiate between type of user

    Methods:
    -__str__: Returns string value of user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    publisher_subscribed = models.ManyToManyField(Publisher, blank=True)
    journalist_subscribed = models.ManyToManyField('self', blank=True, symmetrical=False)
    articles_published = models.ManyToManyField(Article, blank=True)
    newsletters_published = models.ManyToManyField(Newsletter, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.groups.clear()

        # Checks users role and clears data if needed
        if self.role == 'reader':
            group, created = Group.objects.get_or_create(name='Reader')
            self.articles_published.clear()
            self.newsletters_published.clear()
        elif self.role == 'editor':
            group, created = Group.objects.get_or_create(name='Editor')
            self.publisher_subscribed.clear()
            self.journalist_subscribed.clear()
        elif self.role == 'journalist':
            group, created = Group.objects.get_or_create(name='Journalist')
            self.publisher_subscribed.clear()
            self.journalist_subscribed.clear()

        self.user.groups.add(group)
