from django.urls import path

from .views import post_detail, post_list, PostListView, post_share, post_comment, comment_detail, post_search

app_name = 'blogger'

urlpatterns = [
    path('', post_list, name='list'),
    path('tag/<slug:tag_slug>/', post_list, name='Post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='detail'),
    path('<int:post_id>/share', post_share, name='post_share'),
    path('<int:post_id>/comment', post_comment, name='post_comment'),
    path('<int:post_id>/<int:comment_id>', comment_detail, name='comment_detail'),
    path('search/', post_search, name='post_search'),
]
