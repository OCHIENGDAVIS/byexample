from django.urls import path


from .views import post_detail, post_list

app_name = 'blogger'

urlpatterns =[
    path('', post_list, name='list'),
    path('<int:id>/detail', post_detail, name='detail')
]