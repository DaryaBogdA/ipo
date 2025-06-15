from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('about_i', views.about_i, name='about_i'),
    path('about_shop', views.about_shop, name='about_shop'),
    path('spec/', views.spec, name='spec'),
    path('spec/<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('catalog/', views.product_list, name="catalog"),
    path('catalog/<int:pk>/', views.NewsDetailView.as_view(), name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('registration/', views.registration, name='registration'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

]
