from django.utils import timezone
from django.db import models
from students.models import Student


class Testing(models.Model):
    test_name = models.CharField(max_length=40)
    description = models.TextField()
    all_time_opened = models.BooleanField(default=False)
    test_opening_date = models.DateTimeField()
    test_closing_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.test_name


class MultiChoiceQuestion(models.Model):
    task = models.CharField(max_length=30)
    question_name = models.CharField(max_length=20)
    question = models.CharField(max_length=200)
    test = models.ForeignKey(Testing, related_name='multis', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_name


class MatchTask(models.Model):
    test = models.ForeignKey(Testing,related_name='matches', on_delete=models.CASCADE, default=None)
    task = models.CharField(max_length=30)
    match_task_name = models.CharField(max_length=20)

    def __str__(self):
        return self.match_task_name

    class Meta:
        verbose_name_plural = 'Matching tasks'


class Choice(models.Model):
    question = models.ForeignKey(MultiChoiceQuestion, related_name='multis_choices', on_delete=models.CASCADE, default=None)
    choice_text = models.CharField(max_length=200)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class MatchQuestion(models.Model):
    question_text = models.CharField(max_length=50, default=None)
    match_task = models.ForeignKey(MatchTask, related_name='match_options', on_delete=models.CASCADE, default=None)
    choice = models.CharField(max_length=50, default=None)
    points = models.IntegerField(default=1)

    def __str__(self):
        return 'Option'

class TFStatement(models.Model):
    statement = models.CharField(max_length=50)
    tf = models.BooleanField(name='True?')
    test = models.ForeignKey(Testing, related_name='tf_tasks', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.statement


class WordBoxTask(models.Model):
    task_name = models.CharField(max_length=30)
    test = models.ForeignKey(Testing, related_name='word_boxes', on_delete=models.CASCADE)
    without_wordbox = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name


class Sentence(models.Model):
    question_text = models.CharField(max_length=50, default=None)
    match_task = models.ForeignKey(WordBoxTask, related_name='sentences', on_delete=models.CASCADE, default=None)
    choice = models.CharField(max_length=50, default=None)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text
