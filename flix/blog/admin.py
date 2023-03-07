from django.contrib import admin

# Register your models here.

from .models import Movie , TV,TVComment,MovieComment

class MovieAdmin(admin.ModelAdmin):
    list_filter = ("year", "date",)
    list_display = ("name", "year", "cast",)
    prepopulated_fields = {"slug": ("name",)}

class TVAdmin(admin.ModelAdmin):
    list_filter = ("year", "date",)
    list_display = ("name", "year", "cast",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Movie, MovieAdmin)
admin.site.register(TV, TVAdmin)
admin.site.register(TVComment)
admin.site.register(MovieComment)
