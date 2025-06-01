from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about_i', views.about_i, name='about_i'),
    path('about_shop', views.about_shop, name='about_shop'),
    path('spec/', views.spec, name='spec'),
    path('spec/<int:skill_id>/', views.skill_detail, name='skill_detail'),
]
