from django import forms
from .models import Product, Comment, Hashtag


class SearchForm(forms.Form):
    query = forms.CharField(label='검색', max_length=100)


class ProductForm(forms.ModelForm):
    hashtags = forms.CharField(required=False, help_text="해시태그를 쉼표로 구분하여 입력하세요.")

    class Meta:
        model = Product
        fields = ['title', 'content', 'image', 'hashtags']
        # exclude = ("author","like_users", "view")

    def clean_hashtags(self):
        hashtags = self.cleaned_data['hashtags']
        hashtag_list = [tag.strip() for tag in hashtags.split(',')]
        for tag in hashtag_list:
            if not tag.isalnum():  # 특수문자 및 공백 검증
                raise forms.ValidationError("해시태그는 공백이나 특수문자를 포함할 수 없습니다.")
        return hashtag_list


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("article", "user")
