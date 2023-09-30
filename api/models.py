from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_rating(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)

    def avg_rating(self):
        stars_sum = 0
        ratings = Rating.objects.filter(meal=self)
        for rate in ratings:
            stars_sum += rate.stars
        if len(ratings) > 0:
            return stars_sum / len(ratings)
        else:
            return 0

    def __str__(self) -> str:
        return self.title


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # def __str__(self) -> str:
    #     return self.meal.title

    class Meta:
        unique_together = (("user", "meal"),)
        index_together = (("user", "meal"),)
