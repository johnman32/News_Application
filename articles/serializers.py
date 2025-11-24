from rest_framework import serializers
from .models import Article, Newsletter
from publishers.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for existing Publisher Model"""
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'logo', 'description']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for existing Article Model"""
    publisher_name = serializers.CharField(source='published_by.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'date_uploaded',
            'category',
            'published_by',
            'publisher_name',
            'author',
            'author_name',
            'image',
            'status',
        ]
        read_only_fields = ['id', 'author', 'author_name', 'publisher_name', 'date_uploaded']


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for existing Newsletter model"""
    publisher_name = serializers.CharField(source='published_by.name', read_only=True)
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = Newsletter
        fields = [
            'id',
            'title',
            'description',
            'date_sent',
            'published_by',
            'publisher_name',
            'subscriber_count'
        ]

    def get_subscriber_count(self, obj):
        """returns number of subscribers"""
        return obj.subscribers.count()
