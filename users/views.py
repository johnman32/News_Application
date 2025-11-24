from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group


def journalist_detail(request, pk):
    """
    View to display a journalist's profile and their published work
    """
    journalist_profile = get_object_or_404(UserProfile, pk=pk, role='journalist')
    articles = journalist_profile.articles_published.all().order_by('-date_uploaded')
    newsletters = journalist_profile.newsletters_published.all().order_by('-date_sent')

    return render(request, 'users/journalist_detail.html', {
        'journalist': journalist_profile,
        'articles': articles,
        'newsletters': newsletters
    })


@login_required
def subscribe_to_journalist(request, pk):
    """
    View to subscribe to journalist
    """

    journalist = get_object_or_404(UserProfile, pk=pk, role='journalist')
    user_profile = request.user.profile

    user_profile.journalist_subscribed.add(journalist)
    return redirect('journalist_detail', pk=pk)


@login_required
def unsubscribe_from_journalist(request, pk):
    """
    View to unsubscribe to journalist
    """

    journalist = get_object_or_404(UserProfile, pk=pk, role='journalist')
    user_profile = request.user.profile

    user_profile.journalist_subscribed.remove(journalist)
    return redirect('journalist_detail', pk=pk)


def register_user(request):
    """
    View to register a new user

    Parameters
    - request: HTTP request object
    - returns: Redirect on completion
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not username or not password or not email or not role:
            messages.error(request, "Please fill out all the fields")
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            print("USERNAME EXISTS!")
            messages.error(request, "Username already exists")
            return render(request, 'users/register.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        group = Group.objects.get(name=role.title())
        user.groups.add(group)

        login(request, user)
        return redirect('view_articles')

    return render(request, 'users/register.html')


def login_user(request):
    """
    View to log in a user.
    Parameters:
    - request: HTTP request object
    - Returns: Redirects to store list page upon successful login
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_articles')
    return render(request, 'users/login.html')


def logout_user(request):
    """
    View to log out user
    """
    if request.method == 'POST':
        logout(request)
        return redirect('login.html')
