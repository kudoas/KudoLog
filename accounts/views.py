from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from blog.models import Post, Comment
from .forms import UserCreateForm, ProfileCreateForm, RenameForm, IconForm, LoginForm
from .models import User


class Login(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


def signup(request):
    signup_form = UserCreateForm(request.POST or None)

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('blog:post_list')
        else:
            return render(request, 'accounts/sign_up.html', {'form': signup_form})

    if request.method == "POST" and signup_form.is_valid():
        user = signup_form.save(commit=False)
        user.display_name = user.username
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('accounts:signup_done')
    else:
        return render(request, 'accounts/sign_up.html', {'form': signup_form})


class SignupDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    late_posts = user.post_set.order_by('-created_date').reverse()[:3]
    num_posts = user.post_set.order_by('-created_date').count
    profile_form = ProfileCreateForm(
        request.POST, request.FILES or None, instance=user
    )
    rename_form = RenameForm(request.POST or None, instance=user)
    icon_form = IconForm(request.POST, request.FILES or None, instance=user)

    if request.method == 'GET' and request.user.id == user_id:
        rename_form.fields['display_name'].widget.attrs['value'] = request.user.display_name
        profile_form.fields['favorite_word'].widget.attrs['value'] = request.user.favorite_word
        context = {
            'user': user,
            'rename_form': rename_form,
            'profile_form': profile_form
        }

    # rename_formn
    if request.method == "POST" and request.user.id == user_id and rename_form.is_valid():
        user.display_name = rename_form.cleaned_data['display_name']
        user.save()
        return redirect('accounts:edit_profile', user_id=user_id)

    # icon_form
    if request.method == "POST" and request.user.id == user_id and icon_form.is_valid():
        user.icon = icon_form.cleaned_data['icon']
        user.save()
        return redirect('accounts:edit_profile', user_id=user_id)

    # profile_form
    if request.method == "POST" and request.user.id == user_id and profile_form.is_valid():
        user.gender = profile_form.cleaned_data['gender']
        user.birth_year = profile_form.cleaned_data['birth_year']
        user.birth_month = profile_form.cleaned_data['birth_month']
        user.location = profile_form.cleaned_data['location']
        user.favorite_word = profile_form.cleaned_data['favorite_word']
        user.save()
        return redirect('accounts:edit_profile', user_id=user_id)
    context = {
        'profile_form': profile_form,
        'rename_form': rename_form,
        'icon_form': icon_form,
        'num_posts': num_posts,
        'late_posts': late_posts
    }
    return render(request, 'accounts/profile_edit.html', context)


def detail_profile(request, post_id):
    post = Post.objects.get(id=post_id)
    user = post.author
    late_posts = user.post_set.order_by('-created_date').reverse()[:3]
    num_posts = user.post_set.all().count
    context = {
        'post': post,
        'user': user,
        'late_posts': late_posts,
        'num_posts': num_posts
    }
    return render(request, 'accounts/profile_detail.html', context)
