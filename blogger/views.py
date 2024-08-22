from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


from taggit.models import Tag


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


def post_list(request, tag_slug=None):
    all_posts = Post.objects.all()
    tag = None 
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page', 1)
    try:
        all_posts = paginator.page(page_number)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)
    ctx = { 'posts': all_posts}
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


def post_share(request, post_id):
    """Sharing of a post via an email"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('blogger:list'))

    else:
        form = EmailPostForm()
    ctx = {'form': form}
    return render(request, 'blogger/share.html', context=ctx)


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        print('the forms just got saved')
        return HttpResponseRedirect(post.get_absolute_url())
    ctx = {'post': post, 'form': form, 'comment': comment}
    print(ctx)
    return render(request, 'blogger/comment.html', context=ctx)


def comment_detail(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, post=post, id=comment_id)
    ctx = {'post': post, 'comment': comment}
    return render(request, 'blogger/comment_detail.html', context=ctx)


def post_search(request):
    form = SearchForm()
    query = None 
    results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_query = SearchQuery(query)
            search_vector = SearchVector('title', 'body')
            results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    ctx = {
        'form': form,
        'query': query,
        'results': results
    }

    return render(request, 'blogger/search.html', context=ctx)
     
