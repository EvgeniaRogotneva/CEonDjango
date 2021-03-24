from .models import TimeAndCourse
from django.forms import ModelForm, NumberInput, Select, SelectDateWidget, Form, CharField, DateTimeInput, DateField
from django.core.exceptions import ValidationError
from .all_currencies import all_currencies
from datetime import datetime, date, time
import pytz


def time_in_past_or_present(timestamp):
    now = datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)
    if type(timestamp) == date:
        now_time = time()
        added = datetime.combine(timestamp, now_time)
        added = added.replace(tzinfo=pytz.utc)
    else:
        added = timestamp.replace(tzinfo=pytz.utc)
    if added > now:
        return False
    return True


class Validate(Form):
    '''
    def is_valid(self):
        if super().is_valid():
            if not time_in_past_or_present(self.cleaned_data['time']):
                super().add_errors('time', 'date should be in past or present, not future')
                return False
            if not self.cleaned_data['rate'] > 0:
                super().add_errors('rate', 'rate should be bigger than zero')
                return False
            return True
    '''

    def clean_time(self):
        if not time_in_past_or_present(self.cleaned_data['time']):
            raise ValidationError('date should be in past or present, not future')
        return self.cleaned_data['time']

    def clean_rate(self):
        if self.cleaned_data['rate'] <= 0:
            raise ValidationError('rate should be bigger than zero')
        return self.cleaned_data['rate']


class AddRate(ModelForm, Validate):
    class Meta:
         model = TimeAndCourse
         fields = ["currency_code", "time", "rate"]
         widgets = {"currency_code": Select(choices=all_currencies, attrs={'class': 'form-control'}),
                    "time": DateTimeInput(attrs={'class': 'form-control', 'placeholder': "2021-03-05 13:19:13+00:00"}),
                    "rate": NumberInput(attrs={'class': 'form-control', 'placeholder': "0.0"}),}


class GetRate(Validate):
    from_currency_code = CharField(widget=Select(choices=all_currencies, attrs={'class': 'form-control'}))
    to_currency_code = CharField(widget=Select(choices=all_currencies, attrs={'class': 'form-control'}))
    time = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))

