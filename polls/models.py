from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=700)
    pub_date=models.DateTimeField('Date published')

    def __str__(self):
        return self.question_text
    
    def published_recently(self): 
        now = timezone.now() 
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        published_recently.admin_order_field = 'pub_date'
        published_recently.boolean = True
        published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    choice_text=models.CharField(max_length=200)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    votes=models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
