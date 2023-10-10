from django.shortcuts import render
from django.views import generic
from .models import Post


# class based views making them re-usable, so try to use
# classes over functions
class PostList(generic.ListView):
    model = Post
    # filter posts, display only published posts to users
    # display in descending order - oldest first
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6
    
