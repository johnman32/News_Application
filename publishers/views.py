from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Article, Publisher
from django.contrib.auth.decorators import login_required
from .forms import PublisherForm


def publisher_detail(request, pk):
    """
    View to display a single publisher's profile and their articles.

    :param request: HTTP request object
    :type request: HTTPRequest
    :param pk: Primary key of the publisher
    :type pk: int
    :returns: Rendered HTML page with publisher details and articles
    :type: HttpResponse
    """
    publisher = get_object_or_404(Publisher, pk=pk)
    articles = Article.objects.filter(published_by=publisher).order_by('-date_uploaded')

    return render(request, 'publishers/publisher_detail.html', {
        'publisher': publisher,
        'articles': articles
    })


def create_publisher(request):
    """
    View to create a new publisher object

    :param request: HTTP request object
    :type request: HTTPRequest
    :returns: Rendered form template or redirect to articles view
    :type: HttpResponse
    """
    if request.method == "POST":
        form = PublisherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("view_articles")

    else:
        form = PublisherForm()
    return render(request, 'publishers/create_publisher.html', {'form': form})


@login_required
def subscribe_to_publisher(request, pk):
    """
    View to subscribe the current user to a publisher

    :param request: HTTP request object
    :type request: HTTPRequest
    :param pk: Primary key of the publisher
    :type pk: int
    :returns: Redirect to the publisher detail page
    :type: HttpResponse
    """
    publisher = get_object_or_404(Publisher, pk=pk)
    user_profile = request.user.profile

    user_profile.publisher_subscribed.add(publisher)
    return redirect('publisher_detail', pk=pk)


@login_required
def unsubscribe_from_publisher(request, pk):
    """
    View to unsubscribe the current user from a publisher

    :param request: HTTP request object
    :type request: HTTPRequest
    :param pk: Primary key of the publisher
    :type pk: int
    :returns: Redirect to the publisher detail page
    :type: HttpResponse
    """
    publisher = get_object_or_404(Publisher, pk=pk)
    user_profile = request.user.profile

    user_profile.publisher_subscribed.remove(publisher)
    return redirect('publisher_detail', pk=pk)
