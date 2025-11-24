from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Publisher, Article, APIClient as APIClientModel
from users.models import UserProfile
from rest_framework.test import APIClient
from django.urls import reverse


class ArticleTestCase(TestCase):
    """Test cases for Article model and views"""

    def setUp(self):
        """Create test data before each test"""

        # Create groups
        self.journalist_group, _ = Group.objects.get_or_create(name='Journalist')
        self.editor_group, _ = Group.objects.get_or_create(name='Editor')
        self.reader_group, _ = Group.objects.get_or_create(name='Reader')

        # Create journalist user
        self.journalist_user = User.objects.create_user(
            username='journalist1',
            password='testpass123',
            email='journalist@test.com'
        )
        self.journalist_user.groups.add(self.journalist_group)

        UserProfile.objects.create(
            user=self.journalist_user,
            role='journalist'
        )

        # Create reader user
        self.reader_user = User.objects.create_user(
            username='reader1',
            password='testpass123'
        )

        UserProfile.objects.create(
            user=self.reader_user,
            role='reader'
        )

        # Create publisher
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='test test test'
        )

        # Create api client
        self.api_client_model = APIClientModel.objects.create(name='Test API Client')
        self.api_client_model.subscribed_journalists.add(self.journalist_user)

        # Initialize test client
        self.client = APIClient()

        self.url = '/articles/api/articles/'

    def test_create_article(self):
        """Test that an article can be created"""
        article = Article.objects.create(
            title='Test Article',
            description='Test content',
            author=self.journalist_user,
            category='Sports',
            published_by=self.publisher,
            status='pending'
        )

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.journalist_user)
        self.assertEqual(article.status, 'pending')

    def test_update_article(self):
        """Test updating an article"""
        # Login as journalist
        self.client.login(username='journalist1', password='testpass123')

        # Create article
        article = Article.objects.create(
            title='Original Title',
            description='Original content',
            author=self.journalist_user,
            category="sports",
            published_by=self.publisher,
            status='pending'
        )

        # Update data
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated content',
            'category': "new category",
            'published_by': self.publisher.id,
        }

        # Send update request
        response = self.client.post(
            reverse('update_article', args=[article.pk]),
            updated_data
        )

        # Refresh from database
        article.refresh_from_db()

        self.assertEqual(article.title, 'Updated Title')
        self.assertEqual(article.description, 'Updated content')
        self.assertIn(response.status_code, [200, 302])

    def test_api_returns_only_subscribed_articles(self):
        """
        Test that API returns only articles from journalists/publishers
        that the third-party API client is subscribed to
        """
        # Create another journalist that the client is not subscribed to
        other_journalist = User.objects.create_user(
            username='other_journalist',
            password='test123'
        )
        other_journalist.groups.add(self.journalist_group)
        UserProfile.objects.create(user=other_journalist, role='journalist')

        # Create article by journalist client IS subscribed to
        subscribed_article = Article.objects.create(
            title='Subscribed Article',
            description='From subscribed journalist',
            author=self.journalist_user,
            published_by=self.publisher,
            category='Technology',
            status='approved'
        )

        # Create article by journalist client is not subscribed to
        non_subscribed_article = Article.objects.create(
            title='Non-Subscribed Article',
            description='From non-subscribed journalist',
            author=other_journalist,
            published_by=self.publisher,
            category='Sports',
            status='approved'
        )

        # Make API request with valid API key
        response = self.client.get(
            self.url,
            HTTP_X_API_KEY=self.api_client_model.api_key
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Verify only subscribed articles are returned
        article_ids = [article['id'] for article in data['articles']]

        self.assertIn(subscribed_article.id, article_ids)
        self.assertNotIn(non_subscribed_article.id, article_ids)
