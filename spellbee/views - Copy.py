from django.shortcuts import render
from .models import BeeWord, Score
from random import randint
from . import beewordpick 

# Create your views here.
chk =None
def home(request):
    return render(request,"Bee/home.html")
def index(request):
    if request.method == 'POST':
        level = request.POST["level"]
        #word = request.POST["word"]
         
        beeword_obj = random_pick(level)
        
        
        if beeword_obj is not None: 
            beewordpick.SpeakWord(beeword_obj.word)
             
            return render(request, "Bee/check.html",{"spellbee": beeword_obj})

    
    print('No Post request')
    return render(request, "Bee/index.html")

def beeword(request, beeword_key):
    if request.method == 'POST':
        word_typed = request.POST["word"]
        spellbee = get_beeword(beeword_key)
        chk=beewordpick.CheckWord(spellbee.word,word_typed)
        temp =0
        try:
            score_new = Score.objects.get(pickword=spellbee)
            temp = score_new.pickidx
            temp += 1 
        except Exception as err:
            print(" Score table retrieve error", err)
            return render(request, "Bee/home.html",{'err': 'Error:'+str(err)})
        if chk:

            score_new.pickidx = temp
            score_new.lastscore=True
            score_new.scoreboard=1
           
        else: 
            score_new.pickidx = temp
            score_new.lastscore=False
            score_new.scoreboard=0
             
        #spellbee.word = word_typed 
        score_new.save()
        return render(request, "Bee/beeword.html", {"spellbee": spellbee, "chk": chk})
    print('No Post request in beeword function')
    return render(request, "Bee/index.html")
    
    
def beeword_id(request,beeword_id):
    
    try:
        fkey = BeeWord.objects.get(id=beeword_id)
        score_data = Score.objects.get(pickword=fkey)
        return render(request, "Bee/score_view.html", {"score_tb": score_data})
    except Exception as err:
        print('Error',err)
     
        return render(request, "Bee/home.html",{'err': 'Error:'+str(err)})

def get_beeword(beeword_id):
    
    return BeeWord.objects.get(id=beeword_id)

def get_level(request):
    beeword_lvl = BeeWord.objects.order_by('level').values('level').distinct()
    print(beeword_lvl)
    return render(request,"Bee/read.html",{"beeword_lvl" : beeword_lvl})

# One time update to initialize Score table  
def scoretb_update(request):
    Bee_fkey = BeeWord.objects.all()
    for i in Bee_fkey:
        try:
            score_new = Score(pickword=i,pickidx=0,lastscore="False",scoreboard=0)
            score_new.save()
        except Exception as err:
            return render(request, "Bee/home.html",{'err': 'Error in table update:'+str(err)})
    return render(request, "Bee/index.html")
def scoretot(request):

    if request.method == 'POST':
        bee_key =0
        inp_word = request.POST["word"]
        try:
            bee_key = BeeWord.objects.get(word=inp_word)
        except Exception as err:
            print('Beeword retrieve object failed ', err)
            return render(request, "Bee/home.html",{'err': 'Error:'+str(err)})
        if bee_key:
            score_bd= Score.objects.get(pickword=bee_key)
            return render(request,"Bee/score_view.html",{"score_tb" : score_bd})
        else:
            beewordpick.SpeakWord('Enter correct word') 
    return render(request,"Bee/scoretot.html")

def scoreboard(request):
    score_bd =[]
    try:
        beeword_lvl = BeeWord.objects.order_by('level').values('level').distinct()
    except Exception as err:
        return render(request, "Bee/home.html",{'err': 'Error in level filtering:'+str(err)})

    #for lvl in ['ONE','TWO','THREE']:
    for lvl in beeword_lvl: 
        diff_lvl = lvl['level'] 
        
        score_bd.append(score_calc(diff_lvl))
        
    
    
    return render(request,"Bee/scoreboard.html", {"score_bd" : score_bd})
class score_board():
    pass
def score_calc(df_level):
    bee_lvl = BeeWord.objects.filter(level=df_level)
    pass_agg, total_test =0,0
    score_bd =score_board()

    for item in bee_lvl:
        try:
            score_data = Score.objects.get(pickword=item)
        except Exception as err:
            return render(request, "Bee/home.html",{'err': 'Error:'+str(err)})
        pass_agg += score_data.scoreboard
        total_test += score_data.pickidx
    if total_test > 0:
        percent = (pass_agg/total_test)*100
    else:
        percent = 0
    if percent > 75:
        stat = 'strong'
    elif percent < 50:
        stat = 'weak'
    else:
        stat = 'average'
    score_bd.percent   = percent
    score_bd.stat   = stat
    score_bd.lvl   = df_level
    score_bd.test   = total_test
     
    return score_bd

def random_pick(df_level):
    
    if df_level in [None,""]:
        dummy = "No words picked! Please choose level"
        beewordpick.SpeakWord(dummy)
        return None   
    else: 
        try:
            lvl_count=BeeWord.objects.filter(level=df_level).count()
            return BeeWord.objects.filter(level=df_level)[randint(0, lvl_count - 1)]
        except Exception as err:
            return render(request, "Bee/home.html",{'err': 'Error:'+str(err)})