from django.urls import path
from .views import CategoryListView, ArticlesListView, ArticlesUpdateView, ArticlesDetailView, ArticlesCreateView, SearchView

app_name = 'blogs'
urlpatterns = [
    path('category-list', CategoryListView.as_view(), name='category-list'),
    path('articles-list/<int:pk>/', ArticlesListView.as_view(), name='articles-list'),
    path('articles-detail/<int:pk>/', ArticlesDetailView.as_view(), name='articles-detail'),
    path('articles/<int:pk>/update/', ArticlesUpdateView.as_view(), name='articles-update'),
    path('articles-add/', ArticlesCreateView.as_view(), name='articles-add'),
    path('search/', SearchView.as_view(), name='search'),

]