from django.shortcuts import render
from rest_framework import viewsets, status, request
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=["POST"])
    def rate_meal(self, request, pk=None):
        if "stars" in request.data and "username" in request.data:
            meal = Meal.objects.get(id=pk)
            stars = request.data["stars"]
            username = request.data["username"]

            try:
                user = User.objects.get(username=username)
                try:
                    rate = Rating.objects.get(user=user, meal=meal)
                    if rate.stars == int(stars):
                        JsonResponse = {
                            "response": f"The {user.username} Has The Same Rate For This {meal.title}"
                        }
                        return Response(JsonResponse, status=status.HTTP_200_OK)
                    else:
                        rate.stars = stars
                        rate.save()
                        JsonResponse = {
                            "response": f"Existing Rating Updated For {meal.title} From {user.username}",
                            "Data": RatingSerializer(rate).data,
                        }
                        return Response(JsonResponse, status=status.HTTP_202_ACCEPTED)
                except Rating.DoesNotExist:
                    # Create a new rating
                    rate = Rating.objects.create(user=user, meal=meal, stars=int(stars))
                    rateSerializer = RatingSerializer(rate)
                    JsonResponse = {
                        "response": f"New Rating Created For {meal.title} From {user.username}",
                        "Data": rateSerializer.data,
                    }
                    return Response(JsonResponse, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                JsonResponse = {"response": "User not found"}
                return Response(JsonResponse, status=status.HTTP_400_BAD_REQUEST)
        else:
            JsonResponse = {"response": "Username Or Stars Not Provided"}
            return Response(JsonResponse, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
