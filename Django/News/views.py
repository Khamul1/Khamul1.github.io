from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .utils import Mymixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Category
from .forms import NewsForm

class HomeNews(ListView, Mymixin):
    model = News
    context_object_name = 'news'
    template_name = 'News/home_news_list.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            context['title'] = Category.objects.get(pk=category_id)
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView, Mymixin):
    model = News
    template_name = 'News/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class AddNews(CreateView):
    form_class = NewsForm
    template_name = 'News/add_news.html'
    login_url ='/admin/'


# def index(request):
#     news = News.objects.all()
#     categories = Category.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#
#     }
#     return render(request, 'News/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'News/category.html', context=context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'News/view_news.html', context=context)

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'News/add_news.html', {'form': form})