from SmartDjango import Analyse
from django.views import View
from smartify import P

from Base.auth import Auth
from Talk.models import Talk, TalkP, CommitP, Commit
from User.models import UserP


class TalkView(View):
    @staticmethod
    @Analyse.r(b=[
        UserP.username
    ])
    @Auth.require_login
    def get(request):
        talk = Talk.get_talk_by_username(**request.d.dict())
        return talk.d()

    @staticmethod
    @Analyse.r(b=[
        TalkP.talk,
        UserP.username
    ])
    @Auth.require_login
    def post(request):
        is_success = False
        try:
            talk = Talk.create(**request.d.dict())
            is_success = True
        except Exception:
            is_success = False

        return dict(
            is_success=is_success,
            talk=talk.d()
        )

    @staticmethod
    @Analyse.r(b=[
        P('tid', 'talkid'),
    ])
    @Auth.require_talker
    def delete(request):
        """ DELETE /api/talk/

        删除talk
        """
        tid = request.d.talkid
        talk = Talk.objects.get(id=tid)
        talk.delete()


class CommitView(View):
    @staticmethod
    @Analyse.r(b=[
        CommitP.commit,
        P('tid', 'talkid').process(int),
        UserP.username,
    ])
    @Auth.require_login
    def post(request):
        """POST /api/commit/

        添加评论
        """

        is_success = False
        try:
            commit = Commit.create(**request.d.dict())

            is_success = True
        except Exception:
            is_success = False

        return dict(
            is_success=is_success,
            commit=commit.d()
        )
