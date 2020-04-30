from django.urls import path

from Talk.api_views import TalkView, TalkContentView

urlpatterns = [
    path('', TalkView.as_view()),
    path('@<int:tid>', TalkContentView.as_view()),
]
