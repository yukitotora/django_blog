from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.PostListView.as_view(), name='blogs'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.AuthorListView.as_view(), name='authors'),
    path('blogger/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('<int:pk>/create/', views.CommentCreate.as_view(), name='comment-create'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/done', views.UserCreateDone.as_view(), name='signup-done'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('category/<int:pk>/', views.PostCategoryList.as_view(), name='post-category-list'),
    path('tag/<int:pk>/', views.PostTagList.as_view(), name='post-tag-list'),
]
