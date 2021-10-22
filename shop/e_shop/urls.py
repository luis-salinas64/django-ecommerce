from django.contrib import admin
from django.urls import path, include


urlpatterns = [

path('admin/', admin.site.urls),
path('e_shop/', include('shop.e_shop.urls')),
path('picture/',admin.site.urls)
]