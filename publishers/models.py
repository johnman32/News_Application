from django.db import models
from django.contrib.auth.models import User


class Publisher(models.Model):
    """
    Model representing a publisher object

    Fields:
    - name: Name of the company
    - logo: JPEG/PNG of company logo
    - description: Details about the publisher
    """
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="publisher_images/", blank=True, null=True)
    description = models.TextField()

    users = models.ManyToManyField(User, blank=True, related_name='publishers')

    def __str__(self):
        """Returns string value of Publisher"""
        return f"{self.name} - {self.description}"
