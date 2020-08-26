from django.shortcuts import render

# Create your views here.
from blog.models import Post, Author, Comment, Category, Tag
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from blog.forms import CommentCreateModelForm, LoginForm, SignUpForm, PostSearchForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.db.models import Q




def index(request):
    # ホームのページの関数ビュー

    # それぞれのコンテンツをカウント
    num_blogs = Post.objects.all().count()
    num_comments = Comment.objects.all().count()
    num_authors = Author.objects.all().count()

    # セッションを利用して訪問回数をカウント
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_blogs': num_blogs,
        'num_comments': num_comments,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class PostListView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET or None)
        if form.is_valid():

            key_word = form.cleaned_data.get('key_word')
            if key_word:
                queryset = queryset.filter(Q(title__icontains=key_word)|Q(content__icontains=key_word))

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            tag = form.cleaned_data.get('tag')
            if tag:
                queryset = queryset.filter(tag__in=tag).distinct()

            author = form.cleaned_data.get('author')
            if author:
                queryset = queryset.filter(author=author)

        return queryset

class PostDetailView(generic.DetailView):
    model = Post

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author

class CommentCreate(generic.CreateView):
    model = Comment
    form_class = CommentCreateModelForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.author = self.request.user
        comment.save()
        return redirect('blog-detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = Post.objects.filter(id=self.kwargs['pk'])
        context['post_list'] = data_list
        return context

class SignUpView(generic.CreateView):
    """ユーザー登録ページ"""
    form_class = SignUpForm
    template_name = 'register/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return redirect('signup-done')

class UserCreateDone(generic.TemplateView):
    """ユーザー登録したよ"""
    template_name = 'register/signup_done.html'

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/logged_out.html'

class PostCategoryList(generic.ListView):
    """カテゴリ一覧のビュー"""
    model = Post

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=category)

class PostTagList(generic.ListView):
    """タグ一覧のビュー"""
    model = Post

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return super().get_queryset().filter(tag=tag)
