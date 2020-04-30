from django.urls import path

from Talk.api_views import CommitView

urlpatterns = [
    path('', CommitView.as_view()),
]
