from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .service import *


# class MovieListView(APIView):

#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#                 rating_user = models.Count("rating", filter=models.Q(rating__ip=get_client_ip(request)))
#             ).annotate(
#                 middle_star = models.Sum(models.F("rating__star")) / models.Count(models.F('rating'))
#             )
#         serializer = MovieListSerializres(movies, many=True)
#         return Response(serializer.data)

# class MovieDetailView(APIView):

#     def get(self, request, pk):
#         movies = Movie.objects.get(id=pk,draft=False)
#         serializer = MovieDetailSerializres(movies)
#         return Response(serializer.data)


#  class ReviewCreateView(APIView):

#     def post(self, request):
#         review = ReviewCreateSerializers(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


# class AddStarRating(APIView):

#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class MovieCreateView(generics.CreateAPIView):

    serializer_class = MovieDetailSerializres


class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializres
    filter_backends = (DjangoFilterBackend, )
    filterser_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
                rating_user = models.Count("rating", filter=models.Q(rating__ip=get_client_ip(self.request)))
            ).annotate(
                middle_star = models.Sum(models.F("rating__star")) / models.Count(models.F('rating'))
            )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializres


class ReviewCreateView(generics.CreateAPIView):

    serializer_class = ReviewCreateSerializers


class AddStarRating(generics.CreateAPIView):

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer




























