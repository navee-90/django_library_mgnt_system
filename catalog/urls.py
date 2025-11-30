from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='login'),
    path('signout/', views.signout_view, name='logout'),

    # Cart
    path('cart/', views.cart_page, name='cart'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Wishlist
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('add-to-wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Orders
    path('order/', views.order_page, name='order_page'),
]
