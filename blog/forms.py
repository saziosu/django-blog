from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # trailing comma must be used
        # otherwise python will read this as a string instead of a tuple - error!
        # which will get an error
        fields = ('body',)

