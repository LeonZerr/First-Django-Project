from django.urls import path 
from .views import UsersListView,UserDetailView,UserRegisterView,UserLoginView,UserLogoutView,ItemCreateView,UserUpdateView
#from .views import HomePageView#
from .views import CustomPasswordChangeView
from . import views

urlpatterns = [
    path('items/', views.item_list, name='item_list'),
    path('carts/', views.cart_list, name='cart_list'), 
    path('users/', UsersListView.as_view(),name="users_list"),
    #path("", HomePageView.as_view(),name="homepage")
    path("",views.home,name="home"),
    path('profile/<slug:username>/', UserDetailView.as_view(), name='profile'),
    path('register/',UserRegisterView.as_view(),name='register'),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    path('items/new/',ItemCreateView.as_view(),name='new-item'),
    path('checkout/<int:cart_id>/', views.checkout, name='checkout'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('delete_item/<int:item_id>/', views.delete_item_from_market, name='delete_item_from_market'),
    path('confirm_delete_account/', views.confirm_delete_account, name='confirm_delete_account'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('profile/<slug:username>/update/', UserUpdateView.as_view(), name='profile_update'),
]