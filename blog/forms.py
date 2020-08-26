from django import forms
from django.forms import ModelForm
from blog.models import Comment, Category, Tag, Author
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class CommentCreateModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class PostSearchForm(forms.Form):
    """検索フォーム"""
    key_word = forms.CharField(
        label='キーワード', required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    category = forms.ModelChoiceField(
        label='カテゴリの選択', required=False,
        queryset=Category.objects.all(),
    )
    tag = forms.ModelMultipleChoiceField(
        label='タグの選択', required=False,
        queryset=Tag.objects.all(),
    )
    author = forms.ModelChoiceField(
        label='投稿者', required=False,
        queryset=Author.objects.all(),
    )
