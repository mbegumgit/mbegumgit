# Importing Libraries


import pyttsx3

def Init():
    engine = pyttsx3.init() # object creation
    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #printing current voice rate
    engine.setProperty('rate', 125)     # setting up new voice rate
    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1
    #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    return engine

def CallEngine(text):
    engine = Init()
    """Speak words"""
    print('Before engine',text)
    engine.say(text)
    
    engine.runAndWait()
    print('after engine')
    engine.stop()

def SpeakWord(text='Nothing picked'):
    """Speak words"""
    print("inside speakword", text)
    
    CallEngine(text)     
    #return text
# 'Checkword with db
def CheckWord(text,typ_word):
    print('Check word text:', text,typ_word)
    # check spelling
    if text == typ_word:
        new_text =text +"You are correct"
        CallEngine(new_text)
        return True   
    else:
        new_text =text +"You are wrong"
        CallEngine(new_text)
        return False
