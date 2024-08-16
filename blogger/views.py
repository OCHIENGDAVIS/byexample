from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView

from .models import Post


def post_list(request):
    all_published_post = Post.active.all()
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        all_posts = paginator.page(page_number)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)
    ctx = {'published': all_published_post, 'posts': all_posts}
    return render(request, 'blogger/list.html', context=ctx)


def post_detail(request, year, month, day, post):
    ctx = {}
    post = get_object_or_404(Post, publish__year=year, publish__month=month, publish__day=day, slug=post)
    ctx['post'] = post
    return render(request, 'blogger/detail.html', context=ctx)


class PostListView(ListView):
    """Alternative Post list view"""
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogger/list.html'
