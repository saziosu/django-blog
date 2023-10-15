from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm



# class based views making them re-usable, so try to use
# classes over functions
class PostList(generic.ListView):
    model = Post
    # filter posts, display only published posts to users
    # display in descending order - oldest first
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    def get(self, request, slug, *arg, **kwarg):
        # only show published posts
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        # only show approved comments, in ascending order
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                # so that we can tell the user that their comment is awaiting
                # approval from admins
                "commented": False,
                "liked": liked,
                "comment_form" : CommentForm(),
            },
        )

    def post(self, request, slug, *arg, **kwarg):
        # only show published posts
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        # only show approved comments, in ascending order
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # get all of the data we posted from our form
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # set email and username for the comment
            # automatically from the user logged in and commenting
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # get the comment from the form but not commited to db yet
            # first need to assign an post to it
            comment = comment_form.save(commit=False)
            comment.post = post
            # after we know what post this is linked to, we'll save it to the db
            comment.save()
        # if the comment form is not valid (missing some entries)
        # we'll just return an empty comment form
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug,)
        # if the post has been already liked
        # and the user clicks the like button, remove the like
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        # when we like or unlike the post it will reload the page
        # This allows us to see the updated likes
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))