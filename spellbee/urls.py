from django.urls import path
from . import views
#path("<int:beeword_id>", views.beeword_id, name="score_view")
#path("scoreboard", views.scoreboard, name="scoreboard")
urlpatterns = [
    path("test",views.index,name="index"),
    path('bee/<int:beeword_key>',views.beeword,name='beeword'),
    path("", views.home, name="home"),
    path("score", views.scoretot, name="scoretot"),
    path("scoreboard", views.scoreboard, name="scoreboard")

]