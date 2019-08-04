from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup/done/', views.SignupDoneView.as_view(), name='signup_done'),
    path('profile/<int:user_id>/edit',
         views.edit_profile, name='edit_profile'),
    path('profile/<int:post_id>/detail/',
         views.detail_profile, name='detail_profile'),
]
