from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    cast = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=True)

# Added Recently
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
    
# Added Recently
    heading = models.CharField(max_length=100, null=True)
    review = models.TextField(null=True)

    slug = models.SlugField(unique=True,db_index=True)
    synopsis = models.TextField()

    def __str__(self) -> str:
        return self.name.upper()



