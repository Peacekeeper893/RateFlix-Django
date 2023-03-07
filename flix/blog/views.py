from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie , TV , MovieComment , TVComment
from django.views.generic import View

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

    stored_post = request.session.get("stored_posts")

    is_saved = False

    if stored_post is not None:
        is_saved = movie.slug in stored_post

    context = {
        "isMovie" : True,
        "content" : movie,
        "form" : movieForm,
        "comments": movie.comments.all().order_by("-id"),
        "isComment": movie.comments.all().count(),
        "saved":is_saved,
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

    
    stored_post = request.session.get("stored_posts")


    if stored_post is not None:
        is_saved = tv.slug in stored_post 
    else:
        is_saved = False 

    tvForm = TVCommentForm()
    context = {
        "isMovie" : False,
        "content" : tv,
        "form" : tvForm,
        "comments": tv.comments.all().order_by("-id"),
        "isComment": tv.comments.all().count(),
        "saved":is_saved,
    }
    return render(request , "blog/single_post.html" , context=context)



class WatchlistView(View):

    def get(self,request):

        # request.session.clear()
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None or len(stored_posts)==0:
            context = {
                "items" : [],
                "hasitems" : False,
            }
        else:
            movies = Movie.objects.filter(slug__in = stored_posts)
            tvs = TV.objects.filter(slug__in = stored_posts)

            # items = movies + tvs

            context = {
                "movies" : movies,
                "tvs" : tvs,
                "hasitems" : True,
            }

        return render(request , "blog/watchlist.html" , context=context)




    def post(self,request):

        stored_posts = request.session.get("stored_posts")

        if stored_posts == None:
            stored_posts = []

        content_id = (request.POST['content_slug'])
        
        if content_id not in stored_posts: 
            stored_posts.append(content_id)
        else:
            stored_posts.remove(content_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/watchlist/")


