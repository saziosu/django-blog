from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Draft'), (1, 'Published'))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # if the User is deleted, all posts from that user are removed
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    # Auto set to the current date/time
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    # allow exerpt to be blank, otherwise required
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # The default status of the post will be draft, unless published
    status = models.IntegerField(choices=STATUS, default=0)
    # Many users can like many different posts, can be blank
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        # order the posts on when they were created
        # the minus '-' means desce
        ordering = ['-created_on']

    def __str__(self):
        # django docs say to define this, returns a string from the class
        # the default is not helpful at all
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
