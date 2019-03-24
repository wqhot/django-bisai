# -*- coding: utf-8 -*-
from django.shortcuts import render
from bisaiMain import initGame,updateResult,getGameList
from django.http import HttpResponse

import sys
# Create your views here.
reload(sys)
sys.setdefaultencoding('utf-8')


def initGames(request):
    if 'server' in request.GET:
        server = request.GET['server']
        initGame(server)
        message='success'
    else:
        message = 'fail'
    return HttpResponse(message)

def undateGame(request):
    if 'server' in request.GET and 'winner' in request.GET and 'gameid' in request.GET:
        server = request.GET['server']

        gameid = request.GET['gameid']
        winner = request.GET['winner']
        try:
            score = int(request.GET['score'])
        except:
            score = 0
        result = updateResult(server, gameid, winner, score)
        if result==1:
            message = 'success'
        else:
            message = 'fail' + str(result)
    else:
        message = 'fail'
    return HttpResponse(message)

def getGameListView(request):
    if 'server' in request.GET:
        server = request.GET['server']
        message=getGameList(server)

    else:
        message = ''
    obj = HttpResponse(message)
    obj['Access-Control-Allow-Origin'] = '*'
    return obj