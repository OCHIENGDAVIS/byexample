from django.urls import path

from .views import post_detail, post_list

app_name = 'blogger'

urlpatterns =[
    path('', post_list, name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='detail')
]
