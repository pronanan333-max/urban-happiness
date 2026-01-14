from . models import Article

from account.models import CustomUser

from django.forms import ModelForm

from django import forms


class ArticleForm(ModelForm):

    class Meta:

        model = Article
        fields = ['title', 'content','image', 'location', 'price', ]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Article.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("ชื่อนี้ถูกใช้ไปแล้ว กรุณาใช้ชื่ออื่น")
        return title


class UpdateUserForm(ModelForm):

    password = None

    class Meta:

        model = CustomUser
        fields = ['email', 'first_name', 'last_name',]
        exclude = ['password1', 'password2',]





