from django.urls import path,include
from .views import home

urlpatterns = [
    path('/todo/', home, name='home'),
    path('detail/<int:pk>/comment/', create_comment, name='create_comment'),
]

