from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('introduction/', views.IntroductionView.as_view(), name='introduction'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.create_post, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post,
         name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',
         views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]
