from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from .forms import BlogCreateForm, CommentCreateForm
from .models import Blog

# Create your views here.
def login_redriect(request):
    return render(request, 'login_redirect.html')
@login_required
def blog_create(request):
    if request.method == 'POST':
        blog_form = BlogCreateForm(request.POST, files=request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            base_slug = f"{slugify(blog_form.cleaned_data.get('title'))}-by-{request.user.pen_name}"
            counter = 1
            while Blog.objects.filter(slug=blog.slug).exists():
                counter += 1
            blog.slug = base_slug + f'-{counter}'
            if blog.status == 'published':
                blog.published_at = timezone.now()
            blog.save()
            print("Blog post saved successfully")
            return render(request, 'login_redirect.html')

        else:
            return render(request, 'blog/blog_create_form.html', {'form':blog_form})
        
    else:
        blog_form = BlogCreateForm()
        return render(request, 'blog/blog_create_form.html', {'form':blog_form})

def recent_blogs(request):
    posts = Blog.objects.select_related('author').all().order_by('-published_at')[:3]
    context = {'posts':posts}
    return render(request, 'recent_blogs.html', context)

def get_blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    # comments = blog.comments.select_related('commentor').all()
    comment_form = CommentCreateForm()
    return render(request, 'blog/blog_detail.html', {'blog':blog, 'comment_form':comment_form})

@require_POST
def add_or_remove_followers(request, pen_name):
    User = get_user_model()
    writer = get_object_or_404(User, pen_name=pen_name)
    current_user = get_object_or_404(User, username=request.user.username)
    print(f"Writer is {writer.username}")
    print(f"User who wants to follow {current_user.username}")
    if current_user in writer.followers.all():
        writer.followers.remove(request.user)
        print(f"{request.user.username} has been successfully removed")
        return render(request, "partial/partial_def.html#follow-action", {'action':'Follow', 'count':writer.followers.count(), 'writer':writer})
    else:
        writer.followers.add(request.user)
        print(f"{request.user.username} has been successfully added")
        return render(request, "partial/partial_def.html#follow-action", {'action':"Unfollow", 'count':writer.followers.count(), 'writer':writer})

   
@csrf_exempt
def add_blog_comment(request, blog_id):
    blog_obj = get_object_or_404(Blog, id=blog_id)
    comment = CommentCreateForm(request.POST)
    comment = comment.save(commit=False)
    comment.commentor = request.user
    comment.blog = blog_obj
    comment.save()
    print("I have saved the comment")
    new_form = CommentCreateForm()
    return render(request, 'partial/partial_def.html#add_comment_response', {'comment':comment, 'blog':blog_obj, "form":new_form})
    

class BlogDetail(ListView):
    model = Blog
    paginate_by = 1
    context_object_name = 'comments'
    def get_template_names(self):
        if self.request.htmx:
            return 'partial/comments_list.html'
        return "blog/blog_detail.html"
    def get_queryset(self):
        blog_slug = self.kwargs.get('blog_slug')
        blog_obj = get_object_or_404(Blog, slug=blog_slug)
        return blog_obj.comments.all().order_by('-created_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_slug = self.kwargs.get('blog_slug')
        blog_obj = get_object_or_404(Blog, slug=blog_slug)
        comment_form = CommentCreateForm()
        context['blog'] = blog_obj
        context['comment_form'] = comment_form
        return context

def blog_list(request):
    blogs = Blog.objects.select_related("author").all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

class BlogList(ListView):
    model = Blog
    paginate_by = 3
    queryset = Blog.objects.all().order_by('-created_at')
    context_object_name = 'blogs'

    def get_template_names(self):
        if self.request.htmx:
            return "partial/partial_blog_list.html"
        return "blog/blog_list.html"
    
    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')
    
    
    
@login_required
def like_and_unlike(request, blog_id):
    blog_obj = Blog.objects.get(pk=blog_id)
    if request.user in blog_obj.likes.all():
        blog_obj.likes.remove(request.user)
        heart = "💚"
        msg = 'Like'
    else:
        blog_obj.likes.add(request.user)
        heart = "❤️"
        msg = "Unlike"
    return render(request, 'partial/partial_def.html#like_and_unlike_response', {'heart':heart, 'msg':msg, 'likes_count':blog_obj.likes.count(), 'blog':blog_obj})
        

@require_GET
@login_required
def search_blog(request):
    search_value = request.GET.get("search_input")
    search_result = Blog.objects.filter(Q(title__icontains=search_value) | Q(author__pen_name__icontains=search_value))
    return render(request, 'partial/search_result.html', {'blogs':search_result})

