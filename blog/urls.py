from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # first slug is path converter, second is a keyword name
    # path converter converts this into a slug field
    # path converters: https://docs.djangoproject.com/en/3.2/topics/http/urls/#how-django-processes-a-request
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
