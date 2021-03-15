from django.db import models
import mysite.settings


class TimeAndCourse(models.Model):
    currency_code = models.CharField(max_length=3, name='currency_code')
    time = models.DateTimeField()
    rate = models.FloatField()

    def __str__(self):
        return 'currency: ' + self.currency_code + ', timestamp: ' + str(self.time) + ', rate: ' + str(self.rate)

