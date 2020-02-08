from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import BlogPost, Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,
                                  DetailView, CreateView,
                                  UpdateView,DeleteView,)
# Create your views here.
class About(TemplateView):
    template_name = 'blog/about.html'

class PostList(ListView):
    model = BlogPost

    def get_queryset(self):
        return BlogPost.objects.filter(published__lte=timezone.now()).order_by('-published')

class PostDetail(DetailView):
    model = BlogPost

class CreatePost(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/blogpost_detail.html'
    form_class = PostForm
    model = BlogPost

class PostUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/blogpost_detail.html'
    form_class = PostForm
    model = BlogPost


class PostDelete(LoginRequiredMixin,DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blogpost_list')

class DraftList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/blogpost_list.html'
    model = BlogPost

    def get_queryset(self):
        return BlogPost.objects.filter(published__isnull=True).order_by('create_date')

################################################
################################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)




def add_comment_to_post(request,pk):
    post = get_object_or_404(BlogPost,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm
        return render(request,'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

