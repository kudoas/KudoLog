from django import forms
from markdownx.widgets import MarkdownxWidget

from .models import Post, Comment


class PostForm(forms.ModelForm):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['text'].widget = MarkdownxWidget()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('text',)
