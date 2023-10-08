from django import forms
from .bulma_mixin import BulmaMixin
from .models import *


class CreateChannelForm(BulmaMixin, forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название канала'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Описание канала'}))
    image = forms.ImageField(label='Аватар')

    class Meta:
        model = HostingСhannel
        fields = ['name', 'description', 'image']


class CreateVideoForm(BulmaMixin, forms.ModelForm):
    preview = forms.ImageField(label='Превью')
    video = forms.FileField(label='Видео')
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Описание'}))

    class Meta:
        model = HostingСhannel
        fields = ['preview', 'video', 'name', 'description']


class EditVideoForm(BulmaMixin, forms.ModelForm):
    preview = forms.ImageField(label='Превью', )
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Описание'}))

    class Meta:
        model = HostingСhannel
        fields = ['preview', 'name', 'description']


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'textarea',
        'size': '40',
        'placeholder': 'Оставьте свой комментарий...'
    }))

    class Meta:
        model = Comment
        fields = ['body', ]


class ParentForm(BulmaMixin, forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите комментарий'}))

    class Meta:
        model = CommentParent
        fields = ['text']


class ComplaintAboutThePostForm(forms.ModelForm):
    violation = forms.ChoiceField(choices=VIOL_CHOICES, required=True, label='Причина жалобы')
    text_violation = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'textarea',
        'size': '60',
        'placeholder': 'Оставьте свою жалобу...'
    }))

    class Meta:
        model = ComplaintAboutThePost
        fields = ['violation', 'text_violation']
