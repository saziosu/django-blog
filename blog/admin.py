from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    # allow slug to be pre-populated from the post title
    prepopulated_fields = {'slug': ('title',)}
    # add filter option to the admin panel
    list_filter = ('status', 'created_on')
    # display these items on the posts in admin panel
    list_display = ('title', 'slug', 'status', 'created_on')
    # allow these terms to be searched in admin panel
    search_fields = ['title', 'content']
    # add summernote editor to the post content field
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    # allow comments to be approved from admin panel view
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
