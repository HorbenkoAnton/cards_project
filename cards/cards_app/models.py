from django.db import models
import datetime
from django.utils import timezone


class Card(models.Model):
    eng_word = models.CharField(max_length=30)
    ukr_word = models.CharField(max_length=50)
    last_time_drafted = models.DateTimeField(default=timezone.now)
    last_result = models.BooleanField(default = False)
    is_draftable = models.BooleanField(default=True)

    def __str__(self):
        return self.eng_word
    
    def unrevise(self):
        self.is_draftable = True

    def update_is_draftable(self):
        now = timezone.now()
        if self.last_result:
            # Ensure that both datetimes are timezone-aware
            if self.last_time_drafted.tzinfo is None:
                self.last_time_drafted = timezone.make_aware(self.last_time_drafted)
            if (now - self.last_time_drafted) < datetime.timedelta(days=2):
                self.is_draftable = False
            else:
                self.is_draftable = True

#What do i want
#System that will remember how often does user remembers that word
#The more times user remembers words the fewer times it will show up
#But as time passes words will be shown up anyways
#Do i need some kin of points?
#I definitely need to update is draftable based on time, or have some points system. 
# To filter draftable words

class InDevCard(models.Model):
    eng_word = models.CharField(max_length=30)
    ukr_word = models.CharField(max_length=50)
