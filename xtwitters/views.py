from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from .forms import TweetForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """Página inicial da xtwitter"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tweets'))
    else:
        return render(request, 'xtwitters/index.html') 


@login_required
def tweets(request):
    """Mostra todos os tweets"""
    tweets = Tweet.objects.order_by('-date_added')
    context = {'tweets': tweets}
    return render(request, 'xtwitters/tweets.html', context)


@login_required
def new_tweet(request):
    """Adiciona um novo tweet."""
    if request.method != 'POST':
        form = TweetForm()

    else:
        form = TweetForm(request.POST)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.author = request.user
            new_tweet.save()
            return HttpResponseRedirect(reverse('tweets'))

    context = {'form': form}
    return render(request, 'xtwitters/new_tweet.html', context)


@login_required
def edit_tweet(request, tweet_id):
    """Edita um tweet existente."""
    tweet = Tweet.objects.get(id=tweet_id)
    previous_page = request.META.get("HTTP_REFERER")

    if tweet.author != request.user:
        raise Http404

    else:
        if request.method != 'POST':
            form = TweetForm(instance=tweet)
    
        else:
            form = TweetForm(instance=tweet, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('tweets'))
    
    context = {'tweet': tweet, 'form': form, 'previous_page': previous_page}
    return render(request, 'xtwitters/edit_tweet.html', context)


def logout_view(request):
    """Faz logout do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """Faz o cadastro de um novo usuário."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tweets'))

    if request.method != 'POST':
        form = UserCreationForm()

    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password= request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    
    context = {'form': form}
    return render(request, 'xtwitters/register.html', context)

@login_required
def my_tweets(request):
    tweets = Tweet.objects.filter(author=request.user).order_by('-date_added')
    context = {'tweets': tweets}
    return render(request, 'xtwitters/my_tweets.html', context)

@login_required
def delete_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    previous_page = request.META.get("HTTP_REFERER")
    if tweet.author != request.user:
        raise Http404
    
    else:
        context = {'tweet': tweet, 'previous_page': previous_page}
        if request.method != 'POST':
            return render(request, 'xtwitters/delete_tweet.html', context)
        else:
            tweet.delete()
            return HttpResponseRedirect(reverse('tweets'))

def like_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
