from django.db import models
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


class Resource(models.TextChoices):
    rate = 'rate'
    user = 'user'


class Access(models.TextChoices):
    read = 'read'
    write = 'write'
    delete = 'delete'


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.CharField(max_length=30, choices=Access.choices, default=Access.read)
    resource = models.CharField(max_length=30, choices=Resource.choices, default=Resource.rate)


class Key(models.Model):
    key = models.CharField(max_length=300, name='key')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
