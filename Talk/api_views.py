from SmartDjango import Analyse, E
from django.views import View
from smartify import P

from Base.auth import Auth
from Talk.models import Talk, TalkP, CommitP, Commit
from User.models import UserP

@E.register()
class TalkError:
    CREAT_TALK = E("创建talk错误")


class TalkView(View):
    @staticmethod
    @Analyse.r(b=[
    ])
    @Auth.require_login
    def get(request):
        talk = Talk.get_talk_by_username(request.user.username)
        return talk.d()

    @staticmethod
    @Analyse.r(b=[
        # TalkP.talk,
        P('talk', 'talk')
    ])
    @Auth.require_login
    def post(request):
        is_success = False
        try:
            print(request.d.talk)
            print(request.user.username)
            talk = Talk.create(request.d.talk, request.user.username)
            talker = talk.talker
            # print(talker.talked)
            talker.change_talked()
            # print(talker.talked)
            is_success = True
        except Exception:
            raise TalkError.CREAT_TALK
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
    ])
    @Auth.require_login
    def post(request):
        """POST /api/commit/

        添加评论
        """

        is_success = False
        try:
            commit = Commit.create(request.d.commit, request.d.tid, request.user.username)
            commit.talk.add_commit_number()
            is_success = True
        except Exception:
            is_success = False

        return dict(
            is_success=is_success,
            commit=commit.d()
        )

    @staticmethod
    @Analyse.r(b=[
        P('tid', 'talkid').process(int),
        P('page', '页码').default(0).process(int),
        P('count', '每页数目').default(0).process(int)
    ])
    @Auth.require_login
    def get(request):
        """GET /api/commit
        获取评论
        :param request:
        :return:
        """

        commits = Commit.get_commit(**request.d.dict('tid', 'page', 'count'))

        return dict(
            commits=commits
        )


class TalkContentView(View):
    @staticmethod
    @Analyse.r(b=[P('tid', 'talkid').process(int), P('page', '页码').default(0).process(int),
                  P('count', '每页数目').default(0).process(int)])
    @Auth.require_login
    def get(request):
        """

        获取此talk的内容及commit
        """
        talk = Talk.objects.get(pk=request.d.tid)
        commits = Commit.get_commit(**request.d.dict('tid', 'page', 'count'))
        return dict(
            talk=talk,
            commits=commits,
        )
