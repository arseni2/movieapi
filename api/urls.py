"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include
from apiapp.views import api_movie_all, api_movie_detail, SearchMovie, home, FilteringMovieGenresYear, email_list, \
    GenreView, AddStarRatingView, RatingFilter, getReviews, Logout, Logoin, delReviews, delMovieBin, CreateMovieBin
from apiapp.views import ReviewCreateView
from rest_framework_simplejwt import views as jwt_views




''' 
/auth/users = Регистрация пользователя POST создаем, GET получаем 
/auth/jwt/create = Получить токен доступа
/auth/users/me = Получить/обновить аутентифицированного пользователя.
/all-profiles = Получить все профили пользователей
/profile/<int:pk> = Обновить аутентифицированного пользователя
'''

urlpatterns = [
    path('api-auth/rating/get/<int:pk>',RatingFilter),
    path('api-auth/delReviews/',delReviews),
    path('api-auth/moviebin/',CreateMovieBin.as_view()),
    path('api-auth/delMovieBin/',delMovieBin),
    path('api-auth/rating', AddStarRatingView.as_view()),
    path('api-auth/genres', GenreView.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/reviews', ReviewCreateView.as_view()),
    path('api-auth/reviews/<int:pk>', getReviews),
    path('api-auth/email',email_list),
    #path('user/', test),
    #path('auth/login/', include('rest_framework_jwt.views.obtain_jwt_token')),
    #path('auth/users/', UserListAPIView.as_view()),
#gets all user profiles and create a new profile
    #path("all-profiles",UserProfileListCreateView.as_view(),name="all-profiles"),
   # retrieves profile details of the currently logged in user
    #path("profile/<int:pk>",userProfileDetailView.as_view(),name="profile"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    #path('account/', include('apiapp.urls')),
    #path('user/', include('users.urls', namespace='users')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/movie', api_movie_all),
    path('api-auth/moviefilter', FilteringMovieGenresYear.as_view()),
    path('api-auth/m', SearchMovie.as_view()),
    path('api-auth/movie/<int:pk>', api_movie_detail),
    path('api-auth/logout', Logout.as_view()),
    path('api-auth/loginuser', Logoin.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', home.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
