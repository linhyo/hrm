from django import forms
from vietskill.models import StaffProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = StaffProfile
        fields = ('name', 'birthday', 'sex', 'position', 'email', 'address', 'phone_number', 'picture')