from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
#from django.urls import reverse_lazy
from django.core.mail import send_mail


from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


def post_detail(request, year, month, day, post):
    print(request.method)
    post = get_object_or_404(Post, 
                             slug=post,
                             publish__day=day,
                             publish__month=month,
                             publish__year=year, 
                             status=Post.Status.PUBLISHED)
    return render(request, 'blog/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            title = f'{cd["name"]} recommends you read {post.title}'
            message = f'{cd["name"]} recommends you read {post.title}. Go to {post_url}. Comment:\n{cd["comment"]}'
            send_mail(title, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})