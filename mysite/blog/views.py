from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from .forms import CreateUserForm, LoginForm, CommentForm 
from django.contrib.auth.decorators import login_required


def user_logout(request):
    logout(request)
    return redirect("blog:html") 


class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('blog:my_login')
    template_name = 'registration/signup.html'
    


def my_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password =  form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect("blog:home")
        else:
            print(form)
    else:
        form = LoginForm()

    data ={
        'form': form,
    }
    return render(request, 'registration/login.html', data)

def home(request):
    return render(request, 'blog/home.html')

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4 
    template_name = 'blog/post/list.html'

# def post_list(request):
#     post_list = Post.published.all()
#    paginitor = Paginator(post_list, 4)
#    page_number = request.GET.get('page', 1)
#     try:
#         posts = paginitor.page(page_number)
#     except:
#         posts = paginitor.page(1)

#     posts = paginitor.page(page_number)
#     return render(request, 'blog/post/list.html', {'posts': posts})




#     posts = Post.objects.all()
#     return render(request,'blog/post/list.html',{'posts': posts})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day

        )
    comments = Comment.objects.filter(post=post)
    likes = Like.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog:post_detail', year=year, month=month, day=day, slug=post.slug)
    else:
        comment_form = CommentForm()

    data = {'post': post, 
            'comments': comments,
            'likes': likes, 
            'comment_form': comment_form,
            }
    return render(request, 'blog/post/detail.html', data)


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    liked, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        liked.delete()

    likes_count =post.likes.count()

    return JsonResponse({'likes_count': likes_count})


@login_required
def dashboard(request, id):
    if request.author.id == id:
        user = get_object_or_404(User, id=id)
    else:
        return redirect("blog:html") 
    
    data = {
          'user': user
      }
     
    return render(request, 'blog/dashboard.html', data)
