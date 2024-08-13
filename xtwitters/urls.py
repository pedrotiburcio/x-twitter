from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('tweets', views.tweets, name="tweets"),
    path('new_tweet', views.new_tweet, name="new_tweet"),
    path('edit_tweet/<tweet_id>', views.edit_tweet, name="edit_tweet"),
    path('login', auth_views.LoginView.as_view(template_name='xtwitters/login.html'), name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('my_tweets', views.my_tweets, name="my_tweets"),
    path('delete_tweet/<tweet_id>', views.delete_tweet, name="delete_tweet"),
    path('like_tweet/<int:pk>', views.like_tweet, name="like_tweet"),
]