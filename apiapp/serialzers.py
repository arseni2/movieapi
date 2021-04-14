from rest_framework import serializers
from apiapp.models import Movie, Genre, Actor, Category, Reviews, Rating, RatingStar, MovieBin
from rest_framework.authtoken.models import Token
from allauth.account.adapter import get_adapter
from django.conf import settings
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model



MyUser = get_user_model()
class MovieBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('movieid', )
class CreateMovieBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieBin
        fields = '__all__'

class RatingStarSerializer(serializers.ModelSerializer):
    class Meta:
       model = RatingStar
       fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = MyUser
       fields = "__all__"


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
class RatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = "__all__"



class TokenS(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name', "image", "age", "description")

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', "id")

class ReviewCreate(serializers.ModelSerializer):
        class Meta:
            model = Reviews
            fields = ("name", "text", "movie", "user")
class ReviewGet(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
class ReviewsGet(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    directors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    category = serializers.StringRelatedField()
    reviews = ReviewsGet(many=True)
    #teto = serializers.SlugRelatedField(
      #  many=True,
       # read_only=True,
      #  slug_field='genres'
   # )
    class Meta:
        model = Movie
        fields = [
            'title', 'tagline', 'description',
                'id',
            'poster', 'year', 'country',
            'directors', 'actors', 'genres',
            'world_premiere', 'budget', 'fees_in_usa',
            'fess_in_world', 'category', 'url',
            'draft','reviews', 'isFollow', 'user'
        ]


'''
class ReviewsSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    class Meta:
        model = Reviews
        fields = ("movie", "name", "text")
   def to_representation(self, instance):
        rep = super(ReviewsSerializer, self).to_representation(instance)
        rep['movie'] = instance.movie.title
        return rep'''