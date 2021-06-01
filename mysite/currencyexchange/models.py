from django.db import models
import mysite.settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import User


class GetRate(models.Manager):

    def get_rate_from_bd_with_date(self, currency_code, time):
        rate = self.filter(currency_code=currency_code).filter(time__lte=time).order_by('-time')
        if rate.first():
            return rate.first()
        return None


class TimeAndCourse(models.Model):
    id = models.AutoField(primary_key=True)
    currency_code = models.CharField(max_length=3, name='currency_code')
    time = models.DateTimeField()
    rate = models.FloatField()
    objects = GetRate()

    class Meta:
        indexes = [
            models.Index(fields=['time'])
        ]

    def __str__(self):
        return 'currency: ' + self.currency_code + ', timestamp: ' + str(self.time) + ', rate: ' + str(self.rate)


class Key(models.Model):
    key = models.CharField(max_length=300, name='key')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
