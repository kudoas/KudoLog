from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from accounts.models import User
from .forms import PostForm, CommentForm
from .models import Comment, Post


class IntroductionView(TemplateView):
    template_name = 'blog/introduction.html'


class PolicyView(TemplateView):
    template_name = 'blog/policy.html'


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-published_date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def create_post(request):
    post_form = PostForm(request.POST or None)
    if request.method == 'POST' and post_form.is_valid:
        post = post_form.save(commit=False)
        if request.user.is_authenticated:
            post.author = request.user
        post.save()
        return redirect('blog:post_draft_list')
    return render(request, 'blog/post_form.html', {'post_form': post_form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and post_form.is_valid():
        post_form.save(commit=False)
        post.published_date = timezone.now()
        post_form.save()
        return redirect('blog:post_detail', pk=pk)
    context = {'post_form': post_form}
    return render(request, 'blog/post_edit.html', context)


@require_POST
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('-created_date')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.author = request.user
                comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail.html', pk=pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)
