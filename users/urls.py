from django.urls import path
from users.views import UserDetail


urlpatterns = [
    path('<int:pk>/', UserDetail.as_view()),
]
