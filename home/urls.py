from django.urls import path
from .views import HomePageTest

urlpatterns = [
    path('', HomePageTest.as_view(), name='home_page'),
]