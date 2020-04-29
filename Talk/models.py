from django.db import models

# Create your models here.
class Talk(models.Model):
    "主题类"
    talk = models.TextField(
    )
    talker = models.ForeignKey(
        'User.User',
        related_name='talker_user',
        on_delete=models.SET_NULL,
        null=True,
    )
    time = models.DateTimeField(
        auto_now=False,
        null=True,
    )
    commit_number = models.IntegerField(
        default=0,
        null=True,
    )

class Commit(models.Model):
    "回复类"
    commit = models.TextField(
    )
    commiter = models.ForeignKey(
        'User.User',
        related_name='commiter_user',
        on_delete=models.SET_NULL,
        null=True,
    )
    talk = models.ForeignKey(
        'Talk.Talk',
        on_delete=models.SET_NULL,
        null=True,
    )
    time = models.DateTimeField(
        auto_now=False,
        null=True,
    )
