from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime
from django.db import models
from datetime import date


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, userPhotos=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            userPhotos=userPhotos,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        arsenij633@gmail.com
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            userPhotos=userPhotos,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    #id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=256, unique=True, null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    userPhotos = models.ImageField(upload_to="userPhotos/", blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'userPhotos']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(id_):
        try:
            return User.objects.get(pk=id_)
        except User.DoesNotExist:
            return None

class fUser(models.Model):
    pass

class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField(upload_to='directors_actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=6)
    isFollow = models.BooleanField(default=False)
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/", unique=True)
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor", null=True)
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.CharField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
    def __str__(self):
        return self.title

class Reviews(models.Model):
    """Отзывы"""
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        '''{"movie": 2, "text": "text", "name": "name"}'''
class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15, null=True)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда", null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", null=True)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
class MovieBin(models.Model):
    moviePoster = models.ImageField("Постер", upload_to="movies/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movieid = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movieBin')

