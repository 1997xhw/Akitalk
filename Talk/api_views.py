from SmartDjango import Analyse, E
from django.views import View
from smartify import P

from Base.auth import Auth
from Base.pager import last_timer
from Talk.models import Talk, TalkP, CommitP, Commit


class TalkView(View):
    @staticmethod
    @Auth.require_login
    def get(request):
        return Talk.get_talk_by_username(request.user.username).d()

    @staticmethod
    @Analyse.r(b=[
        TalkP.talk,
    ])
    @Auth.require_login
    def post(request):
        """ POST /api/talk

        插入talk
        """
        return Talk.create(request.d.talk, request.user).d()

    @staticmethod
    @Auth.require_talker
    def delete(request):
        """ DELETE /api/talk

        删除talk
        """
        Talk.delete_talk(request.user)


class CommitView(View):
    @staticmethod
    @Analyse.r(a=[P('tid', 'talkid').process(int), ], b=[
        CommitP.commit,
    ])
    @Auth.require_login
    def post(request):
        """POST /api/talk/@<int:tid>/commit

        添加评论
        """
        return Commit.create(request.d.commit, request.d.tid, request.user).d()


class TalkContentView(View):
    @staticmethod
    @Analyse.r(a=[P('tid', 'talkid', 'talk').process(int).process(Talk.get_talk_by_pk)],
               b=[P('last', '最后一条commit的时间').default(0, through_processors=True).process(last_timer),
                  P('count', '每页数目').default(5).process(int)])
    @Auth.require_login
    def post(request):
        """POST /api/talk/@<int:tid>

        获取此talk的内容及commit
        """
        return dict(
            talk=request.d.talk.d(),
            commits=Commit.get_commit(**request.d.dict()),
        )
