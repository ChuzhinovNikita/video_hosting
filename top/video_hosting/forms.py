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
