from django.db import models

# Create your models here.
class BeeWord(models.Model):
    level = models.CharField(max_length=10)
    word = models.CharField(max_length=90, unique=True, null=True)
    class Meta:
        db_table = 'beeword_tb'       
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
    pickword = models.ForeignKey(BeeWord, on_delete=models.CASCADE, related_name="wordscore")
    pickidx = models.IntegerField(default=0)
    lastscore = models.BooleanField(default=False)
    scoreboard_pass = models.IntegerField(default=0)
    scoreboard_fail = models.IntegerField(default=0)

    def __str__(self):
        return f"Index -{self.id}: {self.pickword} -- Lastscore is {self.lastscore} & attempted {self.pickidx} times"