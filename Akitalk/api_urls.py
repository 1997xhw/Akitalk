from django.urls import include, path

urlpatterns = [
    path('/base', include('Base.api_urls')),
    path('/user', include('User.api_urls')),
    # path('talk/', include('Talk.talk_api_urls')),
    path('/talk', include('Talk.talk_api_urls')),
    # path('commit/', include('Talk.commit_api_urls')),

]
