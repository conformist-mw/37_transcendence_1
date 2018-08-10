from django.urls import path
from users.views import UserDetail
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('<int:pk>/', UserDetail.as_view()),
    path('<str:username>/', UserDetail.as_view()),
    path('login/', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
]
