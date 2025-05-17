from django.urls import path
from . import views
urlpatterns = [
       path('', views.index, name='home'),
       path('about', views.about_i, name='about_i'),
       path('shop', views.about_shop, name='about_shop'),
]
