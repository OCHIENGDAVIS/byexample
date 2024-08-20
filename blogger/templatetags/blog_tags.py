from django import template
from  django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blogger/latest_post.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('-created')[:count]
    ctx = {
        'latest_posts':latest_posts 
    }
    return ctx

@register.simple_tag
def most_commented_posts():
    most_commented = Post.objects.annotate(total_comment=Count('comments')).order_by('-total_comment')[:2]
    return most_commented