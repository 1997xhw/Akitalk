from django.urls import path

from Talk.api_views import TalkView, CommitView

urlpatterns = [
    path('', TalkView.as_view()),
]
