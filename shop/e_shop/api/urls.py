from django.urls import path

# Importamos las API_VIEWS:
from e_shop.api.api_views import *

urlpatterns = [
    # User APIs:
    path('user/login/', LoginUserAPIView.as_view()),

    
    # Articulos API View:
    path('articulos/get', GetArticuloAPIView.as_view()),
    path('articulos/post', PostArticuloAPIView.as_view()),
    path('articuloss/get-post', ListCreateArticuloAPIView.as_view()),
    path('articulos/<pk>/update', RetrieveUpdateArticuloAPIView.as_view()),
    path('articulos/<pk>/delete', DestroyArticuloAPIView.as_view()),

    # TODO: Wish-list API View
    path('wish/get', GetWishListAPIView.as_view()),
    path('wish/post', PostWishListAPIView.as_view()),

]