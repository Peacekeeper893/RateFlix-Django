from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie , TV
# Create your views here.


def home(request):

    latest_movies = Movie.objects.all().order_by("-date")[:4]
    latest_tv = TV.objects.all().order_by("-date")[:4]
    context = {
        "latest_movies" : latest_movies,
        "latest_tv": latest_tv
    }
    return render(request,"blog/index.html",context=context)

def movies(request):

    all_movies = Movie.objects.all().order_by("-date")

    context = {
        "all_movies" : all_movies
    }

    return render(request,"blog/movies.html" , context=context)

def tv(request):

    all_tvs = TV.objects.all().order_by("-date")

    context = {
        "all_tvs" : all_tvs
    }

    return render(request,"blog/tv.html" , context=context)

def moviePost(request , slug):

    movie = Movie.objects.get(slug=slug)
    context = {
        "content" : movie
    }
    return render(request , "blog/single_post.html" , context=context)

def tvPost(request , slug):
    tv = TV.objects.get(slug=slug)
    context = {
        "content" : tv
    }
    return render(request , "blog/single_post.html" , context=context)


