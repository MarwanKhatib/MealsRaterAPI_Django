from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# Create your views here.


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def rate_meal(self, request, pk=None):
        if "stars" in request.data:
            try:
                meal = Meal.objects.get(id=pk)
            except Meal.DoesNotExist:
                JsonResponse = {"response": f"Meal ID: [{pk}] Doesn't Exist"}
                return Response(JsonResponse, status=status.HTTP_204_NO_CONTENT)
            stars = request.data["stars"]
            if not int(stars) in range(1, 6):
                JsonResponse = {"message": "Stars Should Be Between 1 To 5"}
                return Response(JsonResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                user = request.user
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
        else:
            JsonResponse = {"response": "Username Or Stars Not Provided"}
            return Response(JsonResponse, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {"message": "This Is Not How You should Create\\Update Rating"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {"message": "This Is Not How You should Create\\Update Rating"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action in ["list", "update", "destroy"]:
            # Restrict "list," "update," and "destroy" actions to admin users only
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # Create the user and token

        token = Token.objects.create(user=user)

        # Customize the response to include the token key
        response_data = {
            "token": token.key,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
