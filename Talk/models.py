from django.db import models

# Create your models here.
from User.models import User
from SmartDjango import models, E
from smartify import P


@E.register()
class TalkError:
    CREATE_TALK = E("创建Talk错误")
    CREATE_COMMIT = E("创建Commit错误")
    NO_MATCHED_SENTENCE = E("找不到匹配的句子")
    NOT_FOUND_SENTENCE = E("不存在的句子")
    NOT_FOUND_TAG = E("不存在的标签")
    CREATE_TAG = E("创建标签错误")
    NOT_BELONG = E("不是你的句子")




class Talk(models.Model):
    """主题类"""
    talk = models.TextField(
    )
    talker = models.ForeignKey(
        'User.User',
        related_name='talker_user',
        on_delete=models.CASCADE,
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

    @classmethod
    def get_talk_by_username(cls, username):
        user = User.get_user_by_username(username)
        if (user.talked):
            talk = Talk.objects.get(talker=user)
        else:
            talk = None
        return talk

    @classmethod
    def create(cls, talk, username):
        try:
            talks = cls(
                talk=talk,
                commit_number=0,
                talker=User.get_user_by_username(username),
            )
            talks.save()
        except Exception as err:
            raise TalkError.CREATE_TALK
        return talks


class Commit(models.Model):
    """回复类"""
    commit = models.TextField(
    )
    commiter = models.ForeignKey(
        'User.User',
        related_name='commiter_user',
        on_delete=models.CASCADE,
        null=True,
    )
    talk = models.ForeignKey(
        'Talk.Talk',
        on_delete=models.CASCADE,
        null=True,
    )
    time = models.DateTimeField(
        auto_now=False,
        null=True,
    )

    @classmethod
    def create(cls, commit, tid, username):
        try:
            commits = cls(
                commit=commit,
                commiter=User.objects.get(username=username),
                talk=Talk.objects.get(id=tid),
            )
            commits.save()
        except Exception as err:
            raise TalkError.CREATE_COMMIT
        return commits


class TalkP:
    talk = Talk.get_params('talk')


class CommitP:
    commit = Commit.get_params('commit')
