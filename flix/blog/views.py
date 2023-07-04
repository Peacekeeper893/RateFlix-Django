from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie , TV , MovieComment , TVComment
from django.views.generic import View , ListView
import requests
from slugify import slugify
from datetime import datetime


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

    for movie in response.json()['results'][:9]:

        if movie['original_language'] == "en" :

            info = {}
            slug = slugify(movie['title'] + movie["release_date"])
            info['img'] = IMG_URL + movie["poster_path"]
            if(Movie.objects.filter(slug = slug).exists() == False):
                b = Movie(name= movie["title"] , slug = slug , image = IMG_URL + movie["poster_path"], year = movie["release_date"] )
                b.save()

            info['title'] = movie["title"]
            info['date'] = movie["release_date"]
            info['slug'] = slugify(movie['title'] + movie["release_date"])
            upcoming_list.append(info)
    
    upcoming_list.reverse()

# Getting trending tv shows
    url = "https://api.themoviedb.org/3/trending/tv/week"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1"}
    response = requests.request("GET", url, params=querystring)
    trending_tv = []

    for tv in response.json()['results'][:9]:
        if tv['original_language'] == "en" :
            info = {}
            slug = slugify(tv['name'] + tv["first_air_date"])
            info['img'] = IMG_URL + tv["poster_path"]
            if(TV.objects.filter(slug = slug).exists() == False):
                b = TV(name= tv["name"] , slug = slug , image = IMG_URL + tv["poster_path"], year = tv["first_air_date"] )
                b.save()

            info['title'] = tv["name"]
            info['date'] = tv["first_air_date"]
            info['slug'] = slugify(tv['name'] + tv["first_air_date"])
            trending_tv.append(info)
    
    trending_tv.reverse()

# getting movies by genre
    DISCOVER_URL = '/discover/movie'
    movies_by_genre = {}

    # Action Movies
    url = "https://api.themoviedb.org/3/discover/movie"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1","include_adult":"true","with_genres":"28","sort_by":"popularity.desc"}
    response = requests.request("GET", url, params=querystring)
    movies_by_genre['Action'] = []

    for movie in response.json()['results'][:6]:
        info = {}
        slug = slugify(movie['title'] + movie["release_date"])

        info['img'] = IMG_URL + movie["poster_path"]
        if(Movie.objects.filter(slug = slug).exists() == False):
            b = Movie(name= movie["title"] , slug = slug , image = IMG_URL + movie["poster_path"], year = movie["release_date"] )
            b.save()
        info['title'] = movie["title"]
        info['date'] = movie["release_date"]
        info['slug'] = slug
        movies_by_genre['Action'].append(info)


    # Comedy Movies

    url = "https://api.themoviedb.org/3/discover/movie"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1","include_adult":"true","with_genres":"35","sort_by":"popularity.desc","with_original_language":"en"}

    response = requests.request("GET", url, params=querystring)
    movies_by_genre['Comedy'] = []

    for movie in response.json()['results'][:6]:
        info = {}
        slug = slugify(movie['title'] + movie["release_date"])

        info['img'] = IMG_URL + movie["poster_path"]
        if(Movie.objects.filter(slug = slug).exists() == False):
            b = Movie(name= movie["title"] , slug = slug , image = IMG_URL + movie["poster_path"], year = movie["release_date"] )
            b.save()
        info['title'] = movie["title"]
        info['date'] = movie["release_date"]
        info['slug'] = slug
        movies_by_genre['Comedy'].append(info)



    # Drama Movies

    url = "https://api.themoviedb.org/3/discover/movie"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1","include_adult":"true","with_genres":"18","sort_by":"vote_count.desc","with_original_language":"en"}

    response = requests.request("GET", url, params=querystring)
    movies_by_genre['Drama'] = []

    for movie in response.json()['results'][:6]:
        info = {}
        slug = slugify(movie['title'] + movie["release_date"])
        info['img'] = IMG_URL + movie["poster_path"]
        if(Movie.objects.filter(slug = slug).exists() == False):
            b = Movie(name= movie["title"] , slug = slug , image = IMG_URL + movie["poster_path"], year = movie["release_date"] )
            b.save()
        info['title'] = movie["title"]
        info['date'] = movie["release_date"]
        info['slug'] = slug
        movies_by_genre['Drama'].append(info)
        movies_by_genre['Drama'].reverse()

    # Fantasy Movies

    url = "https://api.themoviedb.org/3/discover/movie"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1","include_adult":"true","with_genres":"14","sort_by":"vote_count.desc","with_original_language":"en"}

    response = requests.request("GET", url, params=querystring)
    movies_by_genre['Fantasy'] = []

    for movie in response.json()['results'][:6]:
        info = {}
        slug = slugify(movie['title'] + movie["release_date"])
        info['img'] = IMG_URL + movie["poster_path"]
        if(Movie.objects.filter(slug = slug).exists() == False):
            b = Movie(name= movie["title"] , slug = slug , image = IMG_URL + movie["poster_path"], year = movie["release_date"] )
            b.save()
        info['title'] = movie["title"]
        info['date'] = movie["release_date"]
        info['slug'] = slug
        movies_by_genre['Fantasy'].append(info)
        movies_by_genre['Fantasy'].reverse()



    context = {

        "upcoming_list": upcoming_list,
        "latest_movies" : latest_movies,
        "latest_tv": latest_tv,
        "highest_tv" : highest_tv,
        "highest_movies" : highest_movies,
        "movies_by_genre":movies_by_genre,
        "trending_tv":trending_tv,

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


#Get the movie
    movie = Movie.objects.get(slug=slug)

#Get the movie id

    url = f"{BASE_URL}/search/movie"
    querystring = {"api_key":API_KEY,"query":f"{movie.name}"}
    response = requests.request("GET", url, params=querystring)
    api_id = response.json()['results'][0]['id']

    print(api_id)

#Save details to the db if not already there

    if(movie.synopsis is None or movie.synopsis == ""):
        url = f"https://api.themoviedb.org/3/movie/{api_id}"
        querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
        response = requests.request("GET", url, params=querystring)
        response = response.json()
        movie.year = response['release_date']
        movie.synopsis = response['overview']
        movie.rating = response['vote_average']
        movie.image = IMG_URL + response['poster_path']
        movie.save()

#Get the movie credits

    detail_url = f"{BASE_URL}/movie/{api_id}/credits"
    querystring2 = {"api_key":API_KEY,"language":"en-US"}
    response2 = requests.request("GET", detail_url, params=querystring2)
    castlist = []
    for cast in response2.json()['cast'][:6]:
        info = {}
        info['name'] = cast['name']
        info['character'] = cast['character']
        try:
            info['img'] = IMG_URL + cast["profile_path"]
        except:
            info['img'] = "https://st4.depositphotos.com/9998432/22597/v/600/depositphotos_225976914-stock-illustration-person-gray-photo-placeholder-man.jpg"
        castlist.append(info)


# Get the video
    url = f"https://api.themoviedb.org/3/movie/{api_id}/videos"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
    response = requests.request("GET", url, params=querystring)
    videokey = ""

    for clip in response.json()['results']:
        if clip["type"] in ["Teaser" , "Trailer"]:
            videokey = clip["key"]
            break
    if(videokey ==""):
        videokey = response.json()['results'][0]["key"]

#Get the recommended movies

    url = f"https://api.themoviedb.org/3/movie/{api_id}/recommendations"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
    response = requests.request("GET", url, params=querystring)
    recommended = []

    for i in response.json()['results'][:6]:
        i['slug'] = slugify(i['title'] + i['release_date'])

        if(Movie.objects.filter(slug = i['slug']).exists() == False):
            b = Movie(name= i["title"] , slug = i['slug'] , image = IMG_URL + i["poster_path"])
            b.save() 

        recommended.append(i)
    
# Handle the comments

    url = f"https://api.themoviedb.org/3/movie/{api_id}/reviews"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1"}
    response = requests.request("GET", url, params=querystring)
    # print(response.text)

    if movie.comments.all().count() == False:

        for i in response.json()['results'][:6]:
            b = MovieComment(user_name= i["author"] , user_email =i["author"] + '@email.com' ,
                           text = i["content"][:min(400 , len(i["content"]))] , movie = movie)
            b.save() 

    if request.method == "POST":
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.save()
            return HttpResponseRedirect( reverse("movies-details-post" , args=[slug]))

    movieForm = MovieCommentForm()

# Check if in the wishlist
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
        "videokey":videokey,
        "recommended":recommended
    }
    return render(request , "blog/single_post.html" , context=context)

def tvPost(request , slug):

    tv = TV.objects.get(slug=slug)


    url = f"{BASE_URL}/search/tv"

    querystring = {"api_key":API_KEY,"query":f"{tv.name}"}
    response = requests.request("GET", url, params=querystring)
    api_id = response.json()['results'][0]['id']
    print(api_id)

    if(tv.synopsis is None or tv.synopsis == ""):
        url = f"https://api.themoviedb.org/3/tv/{api_id}"
        querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
        response = requests.request("GET", url, params=querystring)
        response = response.json()
        tv.year = response['first_air_date']
        tv.synopsis = response['overview']
        tv.rating = response['vote_average']
        tv.image = IMG_URL + response['poster_path']
        tv.save()

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



# Get the video
    url = f"https://api.themoviedb.org/3/tv/{api_id}/videos"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
    response = requests.request("GET", url, params=querystring)
    videokey = ""

    for clip in response.json()['results']:
        if clip["type"] in ["Teaser" , "Trailer"]:
            videokey = clip["key"]
            break
    if(videokey ==""):
        videokey = response.json()['results'][0]["key"]

#Get the recommended movies

    url = f"https://api.themoviedb.org/3/tv/{api_id}/recommendations"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US"}
    response = requests.request("GET", url, params=querystring)
    recommended = []

    for i in response.json()['results'][:6]:
        i['slug'] = slugify(i['name'] + i['first_air_date'])

        if(TV.objects.filter(slug = i['slug']).exists() == False):
            b = TV(name= i["name"] , slug = i['slug'] , image = IMG_URL + i["poster_path"] , year = i["first_air_date"])
            b.save() 

        recommended.append(i)

    url = f"https://api.themoviedb.org/3/tv/{api_id}/reviews"
    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","page":"1"}
    response = requests.request("GET", url, params=querystring)
    # print(response.text)

    if tv.comments.all().count() == False:

        for i in response.json()['results'][:6]:
            b = TVComment(user_name= i["author"] , user_email =i["author"] + '@email.com' ,
                           text = i["content"][:min(400 , len(i["content"]))] , tv = tv)
            b.save() 


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
        "videokey":videokey,
        "recommended":recommended,


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


    url = "https://api.themoviedb.org/3/search/multi"

    querystring = {"api_key":"b41e4cfe8e55ba8de405c85317f02cff","language":"en-US","query":f"{request.GET.get('q')}","page":"1"}
    response = requests.request("GET", url, params=querystring)


    results = response.json()['results'][:5]

    for x in results:
        if x['media_type'] == 'movie':
            x['slug'] = slugify(x['title'] + x['release_date'])
            try:
                if(Movie.objects.filter(slug = x['slug']).exists() == False):
                    b = Movie(name= x["title"] , slug = x['slug'] , image = IMG_URL + x["poster_path"])
                    b.save() 
            except:
                results.remove(x)
        elif x['media_type'] == 'tv':
            x['slug'] = slugify(x['name'] + x['first_air_date'])
            try:
                if(TV.objects.filter(slug = x['slug']).exists() == False):
                    b = TV(name= x["name"] , slug = x['slug'] , image = IMG_URL + x["poster_path"], year = x["first_air_date"] )
                    b.save()
            except:
                results.remove(x)

    print(results)



    has_content = len(results)> 0

    print(has_content)

    context = {
        "has_content": has_content,
        "results": results,
    }

    return render(request, "blog/searchresult.html",context=context)




