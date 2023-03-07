from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    cast = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=True)

    heading = models.CharField(max_length=100, null=True)
    review = models.TextField(null=True)

    slug = models.SlugField(unique=True,db_index=True)
    synopsis = models.TextField()

    def __str__(self) -> str:
        return self.name
    
class TV(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    cast = models.CharField(max_length=100) # Change this to 35 to accomodate styling
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=True)

    heading = models.CharField(max_length=100, null=True)
    review = models.TextField(null=True)

    slug = models.SlugField(unique=True,db_index=True)
    synopsis = models.TextField()

    def __str__(self) -> str:
        return self.name.upper()
    
class MovieComment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE, related_name="comments",null=True)

class TVComment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    season = models.IntegerField(null=True)

    tv = models.ForeignKey(TV, on_delete=models.CASCADE, related_name="comments",null=True)




