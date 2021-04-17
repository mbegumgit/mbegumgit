from django.shortcuts import render, redirect
from .models import BeeWord, Score
from django.contrib.auth.models import User
from random import randint
from . import beewordpick 
from django.contrib import messages

# Create your views here.
chk =None
# def home(request):
#     return render(request,"Bee/home.html")
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
        word_typed = request.POST["word"].lower()
        spellbee = get_beeword(beeword_key)
        chk=beewordpick.CheckWord(spellbee.word,word_typed)
        if request.user.is_authenticated:
            curr_user = request.user

            print("Current User:", curr_user)
        else:
            messages.warning(request, f'User not authenticated.Try Login!')
            return redirect('login')
        temp =0
        try:
            score_new = Score.objects.get(pickword=spellbee, student=curr_user)
            temp = score_new.pickidx
            temp += 1 
        except Exception as err:
            print(" Score table retrieve error", err)   
            messages.error(request, f'Score table retrieve error {err}')
            return redirect('home')
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
        curr_user = request.user
        score_data = Score.objects.get(pickword=fkey,student=curr_user)
        return render(request, "Bee/score_view.html", {"score_tb": score_data})
    except Exception as err:
        print('Error',err)
        messages.error(request, f' table retrieve error {err}')
        return redirect('home')

def get_beeword(beeword_id):
    
    return BeeWord.objects.get(id=beeword_id)

def get_level(request):
    beeword_lvl = BeeWord.objects.order_by('level').values('level').distinct()
    print(beeword_lvl)
    return render(request,"Bee/read.html",{"beeword_lvl" : beeword_lvl})

# One time update to initialize Score table  
def scoretb_update(request, username):
    try:
        
        curr_user = User.objects.get(username=username)
        print('Registered Username:',curr_user)
    except Exception as err:
        print('User retrieve Error:',err)
        messages.error(request, f'User retrieve error for {username}:{err}')
        return redirect('home')
    Bee_fkey = BeeWord.objects.all()
    for i in Bee_fkey:
        try:
            score_new = Score(pickword=i,pickidx=0,lastscore="False",scoreboard=0,student=curr_user)
            score_new.save()
        except Exception as err:
            print('Error in Score table update:',err)
            messages.error(request, f'Error in Score table update for {username}:{err}')
            return redirect('home')
    return redirect('login')

def scoretot(request):

    if request.method == 'POST':
        bee_key =0
        inp_word = request.POST["word"].lower()
        try:
            bee_key = BeeWord.objects.get(word=inp_word)
        except Exception as err:
            print('Beeword retrieve object failed ', err)
            messages.error(request, f'Beeword table retrieve error for {inp_word}:{err}')
            return redirect('home')
        if bee_key:
            if request.user.is_authenticated:
                curr_user = request.user
            else:
                messages.warning(f'User not authenticated!')
                return redirect('login')
            score_bd= Score.objects.get(pickword=bee_key,student=curr_user)
            return render(request,"Bee/score_view.html",{"score_tb" : score_bd})
        else:
            beewordpick.SpeakWord('Enter correct word') 
    return render(request,"Bee/scoretot.html")

def scoreboard(request):
    score_bd =[]
    try:
        beeword_lvl = BeeWord.objects.order_by('level').values('level').distinct()
    except Exception as err:
        print('Error:',err)
        messages.error(request, f'Score board table filter error {err}')
        return redirect('home')
    if request.user.is_authenticated:
        student_name = request.user
    else :
        print('User not authenticated!')
        return redirect('login')
    #for lvl in ['ONE','TWO','THREE']:
    for lvl in beeword_lvl: 
        diff_lvl = lvl['level'] 
        
        score_bd.append(score_calc(diff_lvl, student_name))
    
    score_data={'score_bd': score_bd, 'student_name': student_name}
    
    return render(request,"Bee/scoreboard.html",  score_data )
class score_board():
    pass
def score_calc(df_level,student_name):
    bee_lvl = BeeWord.objects.filter(level=df_level)
    pass_agg, total_test =0,0
    score_bd =score_board()

    for item in bee_lvl:
        try:
            
            score_data = Score.objects.get(pickword=item,student=student_name)
        except Exception as err:
            print('Error:',err)
            messages.error(request, f'Score table retrieve error {err}')
            return redirect('home')
        pass_agg += score_data.scoreboard
        total_test += score_data.pickidx
    if total_test > 0:
        percent = int((pass_agg/total_test)*100)
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
            print('Error:',err)
            messages.error(request, f'BeeWord table retrieve error {err}')
            return redirect('home')