from django import forms
from .models import Publisher
from django.contrib.auth.models import User


class PublisherForm(forms.ModelForm):
    """
    Form to create a new Publisher object

    fields:
    - name: Publishers nae
    - logo: Image uploaded of their logo
    - description: details regarding the publisher
    """
    # Assigns editors/journalist to the publisher
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role__in=['editor', 'journalist']),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select users that are part of your publishing company"
    )

    class Meta:
        model = Publisher
        fields = ['name', 'logo', 'description']
