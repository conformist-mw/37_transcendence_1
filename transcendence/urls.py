from django.contrib import admin
from django.urls import path
from users.views import UserDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/<int:pk>/', UserDetail.as_view()),
]
