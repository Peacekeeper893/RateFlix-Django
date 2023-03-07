from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie , TV , MovieComment , TVComment

from .forms import MovieCommentForm,TVCommentForm
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

    if request.method == "POST":
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.save()
            return HttpResponseRedirect( reverse("movies-details-post" , args=[slug]))

    movieForm = MovieCommentForm()


    context = {
        "isMovie" : True,
        "content" : movie,
        "form" : movieForm,
        "comments": movie.comments.all().order_by("-id"),
        "isComment": movie.comments.all().count(),
    }
    return render(request , "blog/single_post.html" , context=context)

def tvPost(request , slug):

    tv = TV.objects.get(slug=slug)

    if request.method == "POST":
        comment_form = TVCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.tv = tv
            comment.save()
            return HttpResponseRedirect(reverse("tv-details-post" ,args=[slug]))

    
        

    tvForm = TVCommentForm()
    context = {
        "isMovie" : False,
        "content" : tv,
        "form" : tvForm,
        "comments": tv.comments.all().order_by("-id"),
        "isComment": tv.comments.all().count(),
    }
    return render(request , "blog/single_post.html" , context=context)




