from django.db import models

# Create your models here.
class BeeWord(models.Model):
    level = models.CharField(max_length=10)
    word = models.CharField(max_length=90, unique=True, null=True)
    class Meta:
        db_table = 'Spellbeeword_tb'       
        managed = True
    

    def __str__(self):
        return f"Difficulty level {self.level} : {self.word.title()} "

def get_word():
    return BeeWord.objects.get(id=1)
    # 
class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return int(value) # return 0/1

class Score(models.Model):
    pickword = models.ForeignKey(BeeWord,unique=True, on_delete=models.CASCADE, related_name="wordscore")
    pickidx = models.IntegerField(default=0)
    lastscore = models.BooleanField(default=False)
    scoreboard  = models.IntegerField(default=0)
    

    class Meta:
        db_table = 'Spellbeeword_Score_tb'       
        managed = True
    def __str__(self):
        score_string = f"Index -{self.id}: {self.pickword} -- Lastscore is {self.lastscore} & attempted {self.pickidx} times"
        return score_string

class YearList(models.Model):
    pickword = models.ForeignKey(BeeWord, on_delete=models.CASCADE, related_name="yearlist")
    WOC_2021 = models.IntegerField(default=0)
    SOW_2021 = models.IntegerField(default=0)
    WOC_2020 = models.IntegerField(default=0)
    SOW_2020 = models.IntegerField(default=0)