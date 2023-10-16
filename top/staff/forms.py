from django import forms
from .bulma_mixin import BulmaMixin
from users.models import *


# class PunishmentForm(forms.ModelForm):
#     strike = forms.ChoiceField(choices=STRIKE_CHOICES, required=True, label='Наказание')
#
#     class Meta:
#         model = UsersProfile
#         fields = ['strike']
