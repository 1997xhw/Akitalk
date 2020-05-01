from SmartDjango import Analyse, E
from django.views import View
from smartify import P

from Base.auth import Auth
from Base.pager import last_timer
from Talk.models import Talk, TalkP, CommitP, Commit


class TalkView(View):
    @staticmethod
    @Analyse.r(b=[])
    @Auth.require_login
    def get(request):
        return Talk.get_talk_by_username(request.user.username).d()

    @staticmethod
    @Analyse.r(b=[
        TalkP.talk,
    ])
    @Auth.require_login
    def post(request):
        """ POST /api/talk/

        插入talk
        """
        return Talk.create(request.d.talk, request.user).d()

    @staticmethod
    @Analyse.r(b=[
        P('tid', 'talkid'),
    ])
    @Auth.require_talker
    def delete(request):
        """ DELETE /api/talk/

        删除talk
        """
        Talk.delete_talk(request.user)


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
        return Commit.create(request.d.commit, request.d.tid, request.user).d()

    # @staticmethod
    # @Analyse.r(b=[
    #     P('tid', 'talkid').process(int),
    #     P('last', '最后一条commit的时间').default(0).process(last_timer),
    #     P('count', '每页数目').default(5).process(int)
    # ])
    # @Auth.require_login
    # def get(request):
    #     """GET /api/commit
    #     获取评论
    #     """
    #     return Commit.get_commit(**request.d.dict('tid', 'last', 'count'))


class TalkContentView(View):
    @staticmethod
    @Analyse.r(a=[P('tid', 'talkid').process(int)],
               b=[P('last', '最后一条commit的时间').default(0, through_processors=True).process(last_timer),
                  P('count', '每页数目').default(5).process(int)])
    @Auth.require_login
    def post(request):
        """

        获取此talk的内容及commit
        """
        print(request.d.count)
        print(request.d.last)
        return dict(
            talk=Talk.objects.get(pk=request.d.tid).d(),
            commits=Commit.get_commit(**request.d.dict()),
        )
