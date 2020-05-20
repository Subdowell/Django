from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth import get_user_model
User = get_user_model()


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    last_5_posts = Post.objects.all()[:5]
    return render(request, 'blog/post_list.html', {'posts':posts,'last_5_posts': last_5_posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(page=post)
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments})

def static_page(request):
    return render(request, 'blog/static_page.html')

def creat_comment(request):
    new_user = User(first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
    new_user.set_password(request.POST.get('password'))
    new_user.save()
    return render(request, 'blog/static_page.html')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

