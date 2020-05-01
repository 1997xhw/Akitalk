
from django.db import models
from django.utils import timezone
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
        default="",
        null=True,
    )
    talker = models.ForeignKey(
        'User.User',
        related_name='talker_user',
        on_delete=models.CASCADE,
        null=True,
    )
    time = models.DateTimeField(
        # auto_now=False,
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
                time=timezone.now(),
                commit_number=0,
                talker=User.get_user_by_username(username),
            )
            talks.save()
        except Exception as err:
            raise TalkError.CREATE_TALK
        return talks

    def add_commit_number(self):
        self.commit_number = self.commit_number + 1

    def reduce_commit_number(self):
        self.commit_number = self.commit_number - 1

    def d(self):
        return self.dictor('pk->tid', 'talk', 'time', 'commit_number', 'talker')

    def _readable_time(self):
        return self.time.timestamp()

    def _readable_talker(self):
        return self.talker.d()

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
                talk=Talk.objects.get(pk=tid),
            )
            commits.save()

        except Exception as err:
            raise TalkError.CREATE_COMMIT
        return commits

    @classmethod
    def get_commit(cls, tid, page, count):
        try:
            talk = Talk.objects.get(pk=tid)
            commits = Commit.objects.filter(talk=talk)
            if page >= 0 and count > 0:
                start = page * count
                end = start + count
                commits = commits[start: end]

        except:
            pass
        return commits

    def d(self):
        return self.dictor('pk->cid', 'commit', 'time', 'commiter', 'talk')

    def _readable_commiter(self):
        if self.commiter:
            return self.commiter.d()

    def _readable_time(self):
        return self.time.timestamp()

    def _readable_talk(self):
        return self.talk.d()

class TalkP:
    talk, = Talk.get_params('talk')


class CommitP:
    commit, = Commit.get_params('commit')
