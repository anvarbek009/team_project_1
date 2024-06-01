from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Articles, UserArticleInteraction
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ArticlesForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.models import CustomUser
from django.db.models import Q

# Create your views here.


class CategoryListView(View):
    def get(self, request):
        category = Category.objects.all()
        articless = Articles.objects.all()
        context = {
            'category': category,
            'articles': articless
        }
        return render(request, 'blogs/category_list.html', context=context)
    
class ArticlesListView(View):
    def get(self, request, pk):
        articles = Articles.objects.filter(category=pk)
        context = {
            'articles': articles
        }
        return render(request, 'blogs/articles_list.html', context=context)


class ArticlesDetailView(View):
    def get(self, request, pk):
        article = Articles.objects.get(pk=pk)
        return render(request, 'blogs/articles_detail.html', {'article': article})


class ArticlesUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(instance=article)
        context = {
            'update_article_form': update_article_form,
            'article': article
        }
        return render(request, 'blogs/articles_update.html', context=context)

    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(request.POST, request.FILES, instance=article)
        if update_article_form.is_valid():
            update_article_form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('blogs:articles-detail', pk=article.pk)
        else:
            context = {
                'update_article_form': update_article_form,
                'article': article
            }
            return render(request, 'blogs/articles_update.html', context=context)

    def get_success_url(self):
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article updated successfully!")
        return response


class ArticlesCreateView(CreateView):
    model = Articles
    template_name = 'blogs/articles_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article added successfully!")
        return response


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        article = Articles.objects.filter(
            Q(Q(title__icontains=query) | Q(author__username__icontains=query))
        )
        context = {
            'articles': article,
            'query': query
        }
        return render(request, 'blogs/search_results.html', context=context)


@method_decorator(login_required, name='dispatch')
class LikeArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction, crated = UserArticleInteraction.objects.get_or_create(user=request.user, article=article)
        interaction.liked = not interaction.liked
        interaction.save()
        return redirect('blogs:articles-detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class WatchLaterArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        interaction, created = UserArticleInteraction.objects.get_or_create(user=request.user, article=article)
        interaction.watch_later = not interaction.watch_later
        interaction.save()
        return redirect('blogs:articles-detail', pk=pk)


class LikedArticlesView(View):
    def get(self, request):
        interactions = UserArticleInteraction.objects.filter(user=request.user, liked=True)
        articles = [interaction.article for interaction in interactions]
        return render(request, 'blogs/liked_articles.html', {'articles': articles})


class WatchLaterArticlesView(View):
    def get(self, request):
        interactions = UserArticleInteraction.objects.filter(user=request.user, watch_later=True)
        articles = [interaction.article for interaction in interactions]
        return render(request, 'blogs/watch_later_articles.html', {'articles': articles})







