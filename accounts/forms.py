from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import User


class UserCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RenameForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('display_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Please Enter Your Nickname'


class ProfileCreateForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('icon', 'gender', 'birth_year',
                  'birth_month', 'location', 'favorite_word')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def make_select_object(from_x, to_y, dates, increment=True):
        if increment:
            for i in range(from_x, to_y):
                dates.append([i, i])
        else:
            for i in range(from_x, to_y, -1):
                dates.append([i, i])
        return dates

    def make_select_field(select_object):
        dates_field = forms.ChoiceField(
            widget=forms.Select,
            choices=select_object,
            required=False
        )
        return dates_field

    GEMDER_CHOICES = (
        ('', '',),
        ('female', '女性',),
        ('male', '男性',),
        ('not_applicable', '秘密',)
    )
    gender = forms.ChoiceField(
        widget=forms.Select,
        choices=GEMDER_CHOICES,
        required=False
    )

    years = [["", ""]]
    current_year = datetime.now().year
    years = make_select_object(
        current_year, current_year-80, years, increment=False)
    birth_year = make_select_field(years)

    months = [["", ""]]
    months = make_select_object(1, 13, months)
    birth_month = make_select_field(months)

    LOCATION_CHOICES = (
        ('', '',),
        ('北海道', '北海道',),
        ('東北', '東北',),
        ('関東', '関東',),
        ('中部', '中部',),
        ('近畿', '近畿',),
        ('中国', '中国',),
        ('四国', '四国',),
        ('九州', '九州',)
    )
    location = forms.ChoiceField(
        widget=forms.Select,
        choices=LOCATION_CHOICES,
        required=False
    )


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
