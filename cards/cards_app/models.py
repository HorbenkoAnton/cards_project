from django.db import models
import datetime

class Card(models.Model):
    eng_word = models.CharField(max_length=30)
    ukr_word = models.CharField(max_length=50)
    last_time_drafted = models.DateTimeField(default=datetime.datetime.now)
    last_result = models.BooleanField(default = False)
    is_draftable = models.BooleanField(default=True)

    def __str__(self):
        return self.eng_word

    def update_is_draftable(self):
        if self.last_result:
            if self.last_time_drafted - datetime.datetime.now() < datetime.timedelta(days=2):
                self.is_draftable = False
                return
        self.is_draftable = True
        return 