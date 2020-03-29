from django import forms
from markdownx.widgets import MarkdownxWidget
from markdownx.fields import MarkdownxFormField

from .models import Post, Comment


class PostModelForm(forms.ModelForm):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['text'].widget = MarkdownxWidget()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = ('title', 'category', 'text')


CATEGORY_CHOICES = (
    ('general', '一般'),
    ('world', '世の中'),
    ('political economy', '政治と経済'),
    ('living', '暮らし'),
    ('study', '学び'),
    ('technology', 'テクノロジー'),
    ('interesting', 'おもしろ'),
    ('entertainment', 'エンタメ'),
    ('anime&games', 'アニメとゲーム'),
    ('home appliance', '家電'),
)


class PostForm(forms.Form):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['text'].widget = MarkdownxWidget()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    post_img = forms.ImageField(required=False)
    title = forms.CharField(max_length=200)
    category = forms.ChoiceField(
        widget=forms.Select,
        choices=CATEGORY_CHOICES,
        required=True,
    )
    text = MarkdownxFormField(help_text='Markdownに対応しています')


class CategorySearchForm(forms.Form):
    category = forms.ChoiceField(
        widget=forms.Select,
        choices=CATEGORY_CHOICES,
        required=False,
    )


class CommentForm(forms.ModelForm):

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('text',)
