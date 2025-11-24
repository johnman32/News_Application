from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article
from users.models import UserProfile
import requests
from requests_oauthlib import OAuth1


@receiver(post_save, sender=Article)
def article_approval_notification(sender, instance, created, **kwargs):
    """
    Send notifications when article is approved
    Automatically triggered whenever an Article is saved
    """

    if not created and instance.status == 'approved':
        # Send email to subscribers
        notify_subscribers(instance)

        post_to_x(instance)


def notify_subscribers(article):
    """
    Send email notification to all subscribers of the publisher/journalist
    """
    try:
        subscribers = set()

        # Find users subscribed to the publisher
        publisher_subs = UserProfile.objects.filter(
            publisher_subscribed=article.published_by
        )

        # Find users subscribed to the journalist
        if article.author and hasattr(article.author, 'profile'):
            journalist_subs = UserProfile.objects.filter(
                journalist_subscribed=article.author.profile
            )
        else:
            journalist_subs = UserProfile.objects.none()

        # Collect all subscriber emails
        for sub in publisher_subs.union(journalist_subs):
            if sub.user.email:
                subscribers.add(sub.user.email)

        # Send email to all subscribers
        if subscribers:
            subject = f"New article approved: {article.title}"
            message = f"""A new article has been published by
            {article.published_by}.Title: {article.title}
            {article.description[:200]}..."""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                list(subscribers),
                fail_silently=False,
            )

            print(f"Email sent to {len(subscribers)} subscribers")
        else:
            print("No subscribers found, No email sent")

    except Exception as e:
        print(f"Email notification failed: {e}")


def post_to_x(article):
    """
    Post article announcement to X (Twitter) using HTTP API and requests module
    """
    try:
        # Get api settings
        api_key = settings.X_API_KEY
        api_secret = settings.X_API_SECRET
        access_token = settings.X_ACCESS_TOKEN
        access_token_secret = settings.X_ACCESS_TOKEN_SECRET

        # Create OAuth1 authentication
        auth = OAuth1(
            api_key,
            api_secret,
            access_token,
            access_token_secret
        )

        # Prepare tweet text
        tweet_text = f"New Article: {article.title}\n\n"
        tweet_text += f"By {article.published_by}\n"
        tweet_text += f"Category: {article.category}\n\n"

        # Add article description
        max_desc_length = 180 - len(tweet_text)
        if len(article.description) > max_desc_length:
            tweet_text += article.description[:max_desc_length] + "..."
        else:
            tweet_text += article.description

        url = "https://api.twitter.com/2/tweets"

        payload = {
            "text": tweet_text
        }

        # Make the POST request to X API using requests module
        response = requests.post(
            url,
            auth=auth,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check if successful
        if response.status_code == 201:
            tweet_data = response.json()
            tweet_id = tweet_data['data']['id']
            print(f"Successfully posted to X! Tweet ID: {tweet_id}")
        else:
            print(f"X posting failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f" X posting failed: {e}")
