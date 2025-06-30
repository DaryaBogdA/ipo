from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductCategoryViewSet,
    ProducerViewSet,
    CartViewSet,
    CartItemViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'producers', ProducerViewSet)
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart_items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/test-auth/', views.test_auth, name='test_auth'),
    path('api/test-public/', views.public_test, name='public_test'),
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
    path('checkout/', views.checkout, name='checkout'),
]
