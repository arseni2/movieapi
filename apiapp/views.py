from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apiapp.models import Movie, Reviews, Genre, Rating, MovieBin
from apiapp.serialzers import MovieSerializer, ReviewsGet, ReviewCreate, GenreSerializer, \
    CreateRatingSerializer, RatingStarSerializer, RatingSerializer, ReviewGet, UserSerializer, MovieBinSerializer, \
    CreateMovieBinSerializer
from django.http import JsonResponse
from rest_framework import generics, filters
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

import json
'''
можно получать все имена и сравнивать с именем который создаёт пользователь если они равны то нельза сождать акк если же нет то 
можно и можно делать запрос и передавать имя юзера в качестве типа токена уникального пробелы в имени запрешены в качества урла можно слаг
хз насчёт языка
'''
MyUser = get_user_model()
class AddStarRatingView(APIView):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        star = request.data.get('star')
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(star, status=201)
        else:
            return Response(status=400)

class GenreView(APIView):
    def get(self, request):
        reviews = Genre.objects.all()
        review = GenreSerializer(reviews,many=True)
        return Response(review.data)

class ReviewCreateView(APIView):
    """Добавление отзыва к фильму"""
    def post(self, request):
        print(request.user)
        review = ReviewCreate(data=request.data)
        name = request.data.get('name')
        movie = request.data.get('movie')
        text = request.data.get('text')
        movies = Reviews.objects.all().filter(movie=movie)
        serializer1 = ReviewGet(movies, many=True)
        Reviews.objects.create(
            name=name,
            text=text,
            movie_id=movie,
            user_id=request.user.id,
        )

        if review.is_valid():
            review.save()
            name = request.data.get('name')
            text = request.data.get('text')
            movie = request.data.get('movie')
            movies = Reviews.objects.all().filter(movie=movie)
            test = Reviews.objects.latest('id').delete()

            serializer1 = ReviewGet(movies, many=True)
            #data = {"name":name, "text":text}
            return Response(serializer1.data, status=201)
        return Response(serializer1.data, status=201)
@api_view(['GET'])
def getReviews(request, pk):
    movies = Reviews.objects.all().filter(movie=pk)
    serializer = ReviewGet(movies, many=True)
    return Response(serializer.data)


def restruct(d):
    for k in d:
        # convert value if it's valid json
        if isinstance(d[k], list):
            v = d[k]
            try:
                d[k] = json.loads(v[0])
            except ValueError:
                d[k] = v[0]

        # step into dictionary objects to convert string digits to integer
        if isinstance(d[k], dict):
            restruct(d[k])
        elif d[k].isdigit():
            d[k] = int(d[k])

def email_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        email = EmailSendMessage.objects.all()
        serializer = EmailMessageSerializer(email, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name  = request.data.__getitem__("name")
        email = request.data.__getitem__("email")
        serializer = EmailMessageSerializer(data=request.data)
        if serializer.is_valid():
            print(name)
            print(email)
            send_mail('Subject', 'Message.'+name+'welcome', 'admindjango@gmail.com',  [email])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilteringMovieGenresYear(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #search_fields = ["genres__name", "year"]
    #filter_backends = (filters.SearchFilter,)
    #filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genres', 'year']

'''
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        year = self.request.query_params.get('year')
        genres = self.request.query_params.get('genres')
        print(genres)
        print(self.request.GET.getlist('genres'))
        return qs.filter(Q(year=year) | Q(genres__name=genres))#self.queryset.filter(genres__name=i)'''
class Logoin(APIView):
    def get(self, request):
        email = self.request.query_params.get('email')
        print(email)
        user = MyUser.objects.filter(email=email)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class home(APIView):
    #permission_class = [IsAuthenticated]
    def get(self, request):
       email = self.request.query_params.get('email')
       #print(request.user.name)
       # test = User.objects.all()
       #user = MyUser.objects.all()
       user = MyUser.objects.filter(email=email)
       serializer = UserSerializer(user, many=True)
       return Response(serializer.data)

class UserListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
'''думаю стоит сетать юзер айди при загрузке сайта или при аутентификации '''
class CurrentMovieIsFollowing(APIView):
    def post(self, request):
        test = MovieBin.objects.filter(user_id=request.user.id).values()
        for m in test:
            mid = m.get('movieid_id')
            movieAll = Movie.objects.all().filter(id=mid, user_id=request.user.id).update(isFollow = True) #и тут делать доп условие
            print(Movie.objects.all().filter(id=mid).values())
        movik = Movie.objects.all().filter(user_id=request.user.id)
        serializer = MovieBinSerializer(movik, many=True)
        return Response(serializer.data)
class Logout(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def api_movie_all(request):
    if request.method == 'GET':
        print(request.user.id)
        Movie.objects.update(user_id = request.user.id)
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return  Response(serializer.data)
from rest_framework.exceptions import NotFound
@api_view(['GET'])
def api_movie_detail(request, pk):
    global movieid
    if request.method == 'GET':

        movies = Movie.objects.get(id=pk)
        Movie.objects.filter(id=pk).update(user_id=request.user.id)
        try:
            if MovieBin.objects.filter(user_id=request.user.id, movieid_id=pk).values():
                movieid = MovieBin.objects.filter(user_id=request.user.id, movieid_id=pk).values()[0]['movieid_id']
            else:
                movieid = 0
        except MovieBin.DoesNotExist:
            movieid = 0
            print('not found in moviebin ')

        serializer = MovieBinSerializer(movies)
        obj = {
            'movie': serializer.data,
            'mid': movieid
        }
        return Response(obj)

from rest_framework import filters
from django.db.models.functions import Lower
from rest_framework.filters import OrderingFilter


class CaseInsensitiveOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            new_ordering = []
            for field in ordering:
                if field.startswith('-'):
                    new_ordering.append(Lower(field[1:]).desc())
                else:
                    new_ordering.append(Lower(field).asc())
            return queryset.order_by(*new_ordering)

        return queryset
class SearchMovie(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter,CaseInsensitiveOrderingFilter]
    search_fields = ['title', ]


@api_view(['GET'])
def RatingFilter(request, pk):
    if request.method == 'GET':
        rating = get_object_or_404(Rating,movie_id=pk)
        #star = request.data.__getitem__('star')
        serializer = RatingSerializer(rating)
        return Response(serializer.data.__getitem__('star'), status=200)
class userView(APIView):
    #permission_class = [IsAuthenticated]
    def get(self, request):
       print(request.user.id)
       user = False
       if not request.user:
           user = True
       obj = {
           'isUser': user
       }
       return Response(obj)

class CreateMovieBin(APIView):
    def post(self, request):
        movie = Movie.objects.filter(id=request.POST.get('movieid')) # movie.values()[0]['poster'] - poster
        poster = movie.values()[0]['poster']
        userid = request.data.get('userid')
        MovieBin.objects.create(
            user_id = request.user.id,
            moviePoster = poster,
            movieid_id = request.POST.get('movieid')
        )
        test = MovieBin.objects.filter(user_id=request.user.id).values()
        for m in test:
            mid = m.get('movieid_id')
            movieAll = Movie.objects.all().filter(id=mid, user_id=request.user.id).update(
                isFollow=True)  # и тут делать доп условие
            print(Movie.objects.all().filter(id=mid).values())
        movik = Movie.objects.all().filter(user_id=request.user.id)
        serializer = MovieBinSerializer(movik, many=True)
        return Response(serializer.data)
    def get(self, request):
        m = MovieBin.objects.filter(user_id=request.user.id)
        serializer = CreateMovieBinSerializer(m, many=True)
        return Response(serializer.data)
@api_view(['DELETE', 'POST'])
def delReviews(request):
    Reviews.objects.filter(id=request.POST.get('reviews_id'), user=request.user).delete()
    movies = Reviews.objects.all().filter(movie=request.POST.get('movie_id'))
    serializer = ReviewGet(movies, many=True)
    return Response(serializer.data)
@api_view(['DELETE', 'POST'])
def delMovieBin(request):
    MovieBin.objects.filter(movieid_id=request.POST.get('movie_id'), user=request.user).delete()
    movik = Movie.objects.all().filter(user_id=request.user.id)
    serializer = MovieBinSerializer(movik, many=True)
    return Response(serializer.data)


