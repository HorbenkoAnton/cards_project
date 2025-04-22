from django.db import models

class Card(models.Model):
    eng_word = models.CharField(max_length=30)
    ukr_word = models.CharField(max_length=50)
    times_true = models.IntegerField(default=0)
    times_false = models.IntegerField(default=0)
    weight = models.FloatField(blank=True,null=True)

    def drafted_true(self):
        self.times_true +=1
        self.save()
    def drafted_false(self):
        self.times_false+=1
        self.save()

    def save(self, *args, **kwargs):
        self.weight = (1 + self.times_false) / ( 1 + self.times_true)
        super().save(*args, **kwargs) 


    def __str__(self):
        return f"{self.eng_word} - {self.weight}"
