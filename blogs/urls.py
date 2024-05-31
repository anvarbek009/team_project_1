from django.urls import path
from .views import CategoryListView

app_name = 'blogs'
urlpatterns = [
    path('category-list', CategoryListView.as_view(), name='category-list')
]