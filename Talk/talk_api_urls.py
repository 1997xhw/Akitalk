from django.urls import path

from Talk.api_views import TalkView, TalkContentView, CommitView

urlpatterns = [
    path('', TalkView.as_view()),
    path('/@<int:tid>', TalkContentView.as_view()),
    path('/@<int:tid>/commit', CommitView.as_view()),
]
