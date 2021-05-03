from django.db import models
from django.conf import settings

# Create your models here.
class Group(models.Model) :
    group_id = models.AutoField(primary_key=True, unique=True)
    group_name = models.CharField(max_length=50)
    founder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='founder', on_delete=models.CASCADE, blank=True)
    account_owner = models.CharField(max_length = 20)
    account_number = models.CharField(max_length = 20)
    renew_time = models.TimeField(auto_now = False)
    start_date = models.DateField(auto_now = False)
    #in_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __str__(self):
        return self.group_name


class Transactions(models.Model):
    group_id = models.ForeignKey(Group, on_delete = models.CASCADE)
    title = models.CharField(max_length = 20, null = True, blank = True)
    content = models.CharField(max_length = 20, null = True, blank = True)
    money = models.IntegerField(null = True, blank = True)
    balance = models.IntegerField(null = True, blank = True)
    date = models.CharField(max_length = 10)
    memo = models.TextField(null = True, blank = True)

    class Meta:
        ordering = ['-date']

    def summary(self) :
        return self.memo[:50]

    @property
    def founder_name(self) :
        return self.group_id.username


class Notice(models.Model) :
    group_id = models.ForeignKey(Group, on_delete = models.CASCADE, default='1')
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Question(models.Model) :
    group_id = models.ForeignKey(Group, on_delete = models.CASCADE, default='1')
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default = False)

class Answer(models.Model) :
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, null = True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
