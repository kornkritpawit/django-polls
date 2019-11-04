import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def vote_count(self):
        vote = 0
        for choice in self.objects.choice_set.all():
            vote += choice.votes
        return vote 
    # total = models.IntegerField(auto_now = self.vote_count())
    
        

    def __str__(self):
        return self.question_text



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def find_polls_for_text(text):
        quest = Question.objects.filter(question_text__contains=text)
        return quest
    
    def __str__(self):
        return self.choice_text
    