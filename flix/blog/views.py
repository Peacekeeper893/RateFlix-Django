from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie , TV , MovieComment , TVComment
from django.views.generic import View , ListView
import requests


from .forms import MovieCommentForm,TVCommentForm
# Create your views here.


API_KEY = 'b41e4cfe8e55ba8de405c85317f02cff'
BASE_URL = 'https://api.themoviedb.org/3'
IMG_URL = 'https://image.tmdb.org/t/p/w500'


def home(request):

    latest_movies = Movie.objects.all().order_by("-date")[:5]
    latest_tv = TV.objects.all().order_by("-date")[:5]
    highest_tv = (TV.objects.all().order_by("-rating"))[:3]
    highest_movies = Movie.objects.all().order_by("-rating")[:3]

    # Getting the upcoming movies
    UPCOMING_URL = '/movie/upcoming'
    querystring = {"api_key": API_KEY, "language": "en-US"}
    response = requests.request("GET", f"{BASE_URL}{UPCOMING_URL}", params=querystring)
    upcoming_list = []


    for movie in response.json()['results'][:6]:
        info = {}
        info['img'] = IMG_URL + movie["poster_path"]
        info['title'] = movie["title"]
        info['date'] = movie["release_date"]
        upcoming_list.append(info)
        # print(info)


    context = {

        "upcoming_list": upcoming_list,
        "latest_movies" : latest_movies,
        "latest_tv": latest_tv,
        "highest_tv" : highest_tv,
        "highest_movies" : highest_movies

    }
    return render(request,"blog/index.html",context=context)

def movies(request):

    all_movies = Movie.objects.all().order_by("-date")

    context = {
        "all_movies" : all_movies
    }

    # for x in all_movies:
    #     print(x.name)

    return render(request,"blog/movies.html" , context=context)

def tv(request):

    all_tvs = TV.objects.all().order_by("-date")

    context = {
        "all_tvs" : all_tvs
    }

    return render(request,"blog/tv.html" , context=context)

def moviePost(request , slug):

    movie = Movie.objects.get(slug=slug)

    url = f"{BASE_URL}/search/movie"

    querystring = {"api_key":API_KEY,"query":f"{movie.name}"}

    response = requests.request("GET", url, params=querystring)

    api_id = response.json()['results'][0]['id']

    print(api_id)

    detail_url = f"{BASE_URL}/movie/{api_id}/credits"

    querystring2 = {"api_key":API_KEY,"language":"en-US"}

    response2 = requests.request("GET", detail_url, params=querystring2)

    castlist = []

    for cast in response2.json()['cast'][:6]:
        info = {}
        info['name'] = cast['name']
        info['character'] = cast['character']
        info['img'] = IMG_URL + cast["profile_path"]
        castlist.append(info)
        print(info)

    # print(castlist)

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
        "castlist":castlist,
    }
    return render(request , "blog/single_post.html" , context=context)

def tvPost(request , slug):

    tv = TV.objects.get(slug=slug)


    url = f"{BASE_URL}/search/tv"

    querystring = {"api_key":API_KEY,"query":f"{tv.name}"}

    response = requests.request("GET", url, params=querystring)

    api_id = response.json()['results'][0]['id']

    print(api_id)

    detail_url = f"{BASE_URL}/tv/{api_id}/credits"

    querystring2 = {"api_key":API_KEY,"language":"en-US"}

    response2 = requests.request("GET", detail_url, params=querystring2)

    castlist = []

    for cast in response2.json()['cast'][:6]:
        info = {}
        info['name'] = cast['name']
        info['character'] = cast['character']
        info['img'] = IMG_URL + cast["profile_path"]
        castlist.append(info)
        print(info)

    # print(castlist)

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
        "castlist":castlist,
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
    

def SearchResultView(request):

    if request.method == "GET":
        query = request.GET.get("q")
        tvs = TV.objects.filter(name__icontains=query)
        movies = Movie.objects.filter(name__icontains=query)

        has_content = len(movies) + len(tvs) > 0

        print(has_content)

        context = {
            "has_content": has_content,
            "tvs": tvs,
            "movies": movies
        }

        return render(request, "blog/searchresult.html",context=context)




