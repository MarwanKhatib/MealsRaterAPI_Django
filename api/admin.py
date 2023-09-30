from django.contrib import admin
from .models import Meal, Rating

# Register your models here.


class MealAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "no_of_rating", "avg_rating"]
    list_filter = ["title", "description"]
    search_fields = ["title", "description"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "meal", "user", "stars"]
    # Cause the index_together in class Meta I Put index on each Combination to Enhance The Query ANd Filter
    list_filter = ["meal", "user"]


admin.site.register(Meal, MealAdmin)
admin.site.register(Rating, RatingAdmin)
