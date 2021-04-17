from django.urls import path
from . import views
#path("scoretbupdate2021", views.scoretb_update, name="home"),
#path("scoreboard", views.scoreboard, name="scoreboard")
#path("", views.home, name="home"),
urlpatterns = [
    
    path("level",views.get_level , name="read"),
    path("<int:beeword_id>", views.beeword_id, name="score_view"),
    path("test",views.index,name="index"),
    path('bee/<int:beeword_key>',views.beeword,name='beeword'),
    path("scoretb_update/<str:username>", views.scoretb_update, name="tblupdate"),
    path("score", views.scoretot, name="scoretot"),
    path("scoreboard", views.scoreboard, name="scoreboard")
    
]