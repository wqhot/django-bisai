# -*- coding: UTF-8 -*-
from django.db import models
import django.utils.timezone as timezone
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.
class fightHistory(models.Model):
    fightID = models.CharField(max_length=18)
    fightPlayer1 = models.CharField(max_length=8)
    fightPlayer2 = models.CharField(max_length=8)
    fightWinner = models.CharField(max_length=8)
    defScore1 = models.IntegerField(default=0)
    defScore2 = models.IntegerField(default=0)
    fightServer = models.CharField(max_length=10, default='A')
    fightTime = models.DateTimeField(default = timezone.now)
    imgAddress = models.CharField(max_length=50, default=' ')
    fightPlayer1Blood1 = models.IntegerField(default=0)
    fightPlayer1Blood2 = models.IntegerField(default=0)
    fightPlayer2Blood1 = models.IntegerField(default=0)
    fightPlayer2Blood2 = models.IntegerField(default=0)

    def __str__(self):
        return self.fightID+':'+self.fightPlayer1+'vs'+self.fightPlayer2

class Games(models.Model):
    gameServer = models.CharField(max_length=8, default='A')
    gameLun = models.IntegerField(default=0)
    gameNum = models.IntegerField(default=0)
    gamePlayer1ID = models.CharField(max_length=8, default='')
    gamePlayer2ID = models.CharField(max_length=8, default='')
    gameResult = models.CharField(max_length=8,default ='')
    gameScore = models.IntegerField(default=0)
    gameTime = models.DateTimeField(default=timezone.now)
    gameType = models.IntegerField(default=0)
    gameID = models.CharField(max_length=8, default='0')

    def __str__(self):
        return 't'+str(self.gameType)+'g'+ self.gameServer +'r' + str(self.gameLun)+'n' + str(self.gameNum)+ ':'+self.gamePlayer1ID+'vs'+self.gamePlayer2ID

class fightPlayer(models.Model):
    playerID = models.CharField(max_length=8)
    playerScore = models.IntegerField(default=0)
    playerServer = models.CharField(max_length=10, default='A')
    playerLevel = models.IntegerField(default=0)
    playerWinTimes = models.IntegerField(default=0)
    playerFightTimes = models.IntegerField(default=0)
    playerInherit = models.IntegerField(default=0)
    lastUpdateTime = models.DateTimeField(auto_now=True)
    playerNowState=models.CharField(max_length=8,default=0)

    def __str__(self):
        return self.playerID +':g'+str(self.playerNowState)+'s'+str(self.playerScore)