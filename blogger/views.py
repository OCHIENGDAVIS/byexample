from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    all_published_post = Post.active.all()
    all_posts = Post.objects.all()
    ctx = {'published': all_published_post, 'posts': all_posts}
    return render(request, 'blogger/list.html', context=ctx)


def post_detail(request, id):
    ctx ={}
    post = get_object_or_404(Post, id=id)
    ctx['post'] = post
    return render(request, 'blogger/detail.html', context=ctx)