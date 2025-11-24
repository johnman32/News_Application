from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Article, Newsletter


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # --- Journalist group ---
    journalist_group, created = Group.objects.get_or_create(name='Journalist')
    print("Journalist group created")
    editor_group, created = Group.objects.get_or_create(name='Editor')
    print("Editor group created")
    reader_group, created = Group.objects.get_or_create(name='Reader')
    print("Reader group created")

    try:
        # Get article permissions
        content_type = ContentType.objects.get_for_model(Article)
        add_article = Permission.objects.get(codename='add_article', content_type=content_type)
        update_article = Permission.objects.get(codename='change_article', content_type=content_type)
        delete_article = Permission.objects.get(codename='delete_article', content_type=content_type)
        view_article = Permission.objects.get(codename='view_article', content_type=content_type)

        # Get Newsletter permissions

        content_type = ContentType.objects.get_for_model(Newsletter)
        add_newsletter = Permission.objects.get(codename='add_newsletter', content_type=content_type)
        update_newsletter = Permission.objects.get(codename='change_newsletter', content_type=content_type)
        delete_newsletter = Permission.objects.get(codename='delete_newsletter', content_type=content_type)
        view_newsletter = Permission.objects.get(codename='view_newsletter', content_type=content_type)

        # Assign permissions
        journalist_group.permissions.set(
            [add_article,
             delete_article,
             update_article,
             view_article,
             add_newsletter,
             update_newsletter,
             delete_newsletter,
             view_newsletter])

        editor_group.permissions.set(
            [update_article,
             view_article,
             delete_article,
             update_newsletter,
             view_newsletter,
             delete_newsletter])

        reader_group.permissions.set([view_article, view_newsletter])

        print("Permissions assigned successfully")

    except Permission.DoesNotExist as e:
        print(f'Permissions not available yet: {e}')
    except Exception as e:
        print(f"Error setting up {e}")
