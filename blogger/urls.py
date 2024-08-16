from django.urls import path

from .views import post_detail, post_list, PostListView

app_name = 'blogger'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='detail')
]
