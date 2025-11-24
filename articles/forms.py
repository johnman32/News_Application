from django import forms
from .models import Article, Newsletter


class ArticleForm(forms.ModelForm):
    """
    Form to create Article object

    Fields:
    - title: Title of the article
    - description: contents of the article
    - category: what category this articles falls under
    """
    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'published_by', 'image']


class NewsletterForm(forms.ModelForm):
    """
    Form to create newsletter object

    Fields:
    - title: Name of newsletter
    - description: contents of newsletter
    - date_sent: date newsletter is sent out
    - subscribers: Users subscribed to newsletter
    - published_by: User that posted newsletter
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'description', 'published_by']
