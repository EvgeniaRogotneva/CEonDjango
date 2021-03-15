from .models import TimeAndCourse
from django.forms import ModelForm, NumberInput, Select, SelectDateWidget, Form, CharField, DateTimeInput, DateField
from .all_currencies import all_currencies


class TaskForm(ModelForm):
    class Meta:
         model = TimeAndCourse
         fields = ["currency_code", "time", "rate"]
         widgets = {"currency_code": Select(choices=all_currencies, attrs={'class': 'form-control', 'placeholder': "введите три буквы кода валюты"}),
                    "time": DateTimeInput(attrs={'class': 'form-control', 'placeholder': "2021-03-05 13:19:13+00:00"}),
                    "rate": NumberInput(attrs={'class': 'form-control', 'placeholder': "0.0"}),}


class GetRate(Form):
    from_currency_code = CharField(widget=Select(choices=all_currencies, attrs={'class': 'form-control'}))
    to_currency_code = CharField(widget=Select(choices=all_currencies, attrs={'class': 'form-control'}))
    time = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))


