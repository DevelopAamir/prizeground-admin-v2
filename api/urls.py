from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('matches/', views.Matches.as_view()),
    path('join_matches/', views.JoinMatch.as_view()),
    path('load_wallet/', views.LoadWallet.as_view()),
    path('get_coupons/', views.LoadCoupons.as_view()),
 
    path('profile/', views.Profile.as_view())

] 
