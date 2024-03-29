from django.urls import path
from . views import home,movies,tv,moviePost,tvPost,WatchlistView,SearchResultView

urlpatterns = [
    path('', home, name="home"),
    path('search/' , SearchResultView , name="search_result"),
    path('movies/',movies , name="movies-page"),
    path('movies/<slug:slug>',moviePost,name= "movies-details-post"),
    # path('movies')


    path('tv/<slug:slug>',tvPost,name= "tv-details-post"),
    path('tv/',tv , name = "tv-page"),
    path('watchlist/', WatchlistView.as_view(), name = "watchlist"),

]
