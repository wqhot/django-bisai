# -*- coding: UTF-8 -*-
from ggdwj.models import fightPlayer,Games
import math,random,json

def initGame(server):
    try:
        players=fightPlayer.objects.filter(playerServer=server)

    except fightPlayer.DoesNotExist:
        return
    try:
        gggames = Games.objects.filter(gameServer=server)
        gggames.delete()
    except Games.DoesNotExist:
        pass
    playerlist = []
    for play in players:
        playerlist.append({
            'playerID':play.playerID,
            'playerNowState':play.playerNowState
        })
    playerlist2 = range(len(playerlist))
    if len(playerlist)>16:
        diff = len(playerlist) - 4 * math.floor(len(playerlist) / 4)
        diffs = [0, 0, 0, 0]
        i = 0
        while diff > 0:
            diffs[i] = diffs[i] + 1
            i = (i + 1) % 4
            diff = diff - 1
        for i in range(4):
            playerNum = int(len(playerlist) / 4) + diffs[i]
            playGroup = []
            for j in range(playerNum):
                temp1 = random.randint(0, len(playerlist2) - 1)
                playGroup.append(playerlist[playerlist2[temp1]])
                fplayer = fightPlayer.objects.get(playerServer=server,
                                         playerID=playerlist[playerlist2[temp1]]['playerID']
                                         )
                fplayer.playerNowState = i
                fplayer.save()
                playerlist2.remove(playerlist2[temp1])
            count = 0
            for j in range(playerNum-1):
                for k in range(j+1, playerNum):
                    game = Games()
                    game.gameID=server+str(1)+str(i)+str(count)
                    game.gameLun = i
                    game.gameNum = count
                    count = count + 1
                    game.gameServer = server
                    game.gamePlayer1ID = playGroup[j]['playerID']
                    game.gamePlayer2ID = playGroup[k]['playerID']
                    game.gameType = 1
                    game.save()

    else:
        lunshu=math.ceil(math.log(len(playerlist),2))
        flag = True
        temp1 = 0
        temp2 = 0
        player1 = ''
        player2 = ''
        count = 0
        for i in range(len(playerlist)):
            if flag:
                flag = False
                temp1=random.randint(0,len(playerlist2)-1)
                player1 = playerlist[playerlist2[temp1]]['playerID']
                playerlist2.remove(playerlist2[temp1])
                if len(playerlist2) == 0:
                    #print(player1)
                    player2=''
                    game = Games()
                    game.gameID = server + str(0) + str(0) + str(count)
                    game.gameLun = 0
                    game.gameNum = count
                    count = count + 1
                    game.gameServer = server
                    game.gamePlayer1ID = player1
                    game.gamePlayer2ID = player2
                    game.gameResult = player1
                    game.save()
            else:
                temp2 = random.randint(0, len(playerlist2) - 1)
                player2 = playerlist[playerlist2[temp2]]['playerID']
                game = Games()
                game.gameLun = 0
                game.gameNum =count
                game.gameID = server + str(0) + str(0) + str(count)
                count = count + 1
                game.gameServer = server
                game.gamePlayer1ID = player1
                game.gamePlayer2ID = player2
                flag = True
                game.save()
                playerlist2.remove(playerlist2[temp2])


def updateResult(server, gameID, winner, score):
    try:
        game = Games.objects.get(gameServer=server,
                                 gameID = gameID,
                                 gameType = 0
                                 )

    except:
        try:
            game = Games.objects.get(gameServer=server,
                                 gameID = gameID,
                                 gameType = 1
                                 )
            return updateXZSGame(server, gameID, winner, score)
        except:
            return -1
    try:
        player1 = fightPlayer.objects.get(playerServer=server,
                                         playerID=winner
                                         )
    except:
        return -2
    if not(cmp(winner,game.gamePlayer1ID)==0 or cmp(winner,game.gamePlayer2ID)==0):
        return -3
    game.gameResult=winner
    lun = game.gameLun
    num = game.gameNum
    game.save()
    if num%2 == 0:
        otherNum = num + 1
    else:
        otherNum = num - 1
    try:
        game2 = Games.objects.get(gameServer=server,
                                 gameLun = lun,
                                 gameNum = otherNum
                                 )
        print(game2.gameID)
        if len(game2.gameResult)>0:

            newGameID = server + str(0) + str(lun + 1) + str(int(math.ceil(num / 2)))
            try:
                newGame = Games.objects.get(gameServer=server,gameID = newGameID)
            except:
                newGame = Games()
                newGame.gameID =newGameID

            newGame.gameLun = lun + 1
            newGame.gameNum = math.floor(num / 2)
            newGame.gameServer = server
            if num%2 == 0:
                newGame.gamePlayer1ID = winner
                newGame.gamePlayer2ID = game2.gameResult
            else:
                newGame.gamePlayer1ID = game2.gameResult
                newGame.gamePlayer2ID = winner

            newGame.save()
        # elif len(game2.gamePlayer1ID)==0 and len(game2.gamePlayer2ID)==0:
        #     newGameID = server + str(0) + str(lun + 1) + str(int(math.ceil(num / 2)))
        #     try:
        #         newGame = Games.objects.get(gameServer=server, gameID=gameID)
        #     except:
        #         newGame = Games()
        #         newGame.gameID = newGameID
        #     newGame.gameLun = lun + 1
        #     newGame.gameNum = math.floor(num / 2)
        #     newGame.gameServer = server
        #     if num%2 == 0:
        #         newGame.gamePlayer1ID = winner
        #         newGame.gamePlayer2ID = ''
        #     else:
        #         newGame.gamePlayer1ID = ''
        #         newGame.gamePlayer2ID = winner
        #
        #     newGame.gameResult = winner
        #     newGame.save()
    except:
        # newGameID = server + str(0) + str(lun + 1) + str(int(math.ceil(num / 2)))
        # try:
        #     newGame = Games.objects.get(gameServer=server, gameID=gameID)
        # except:
        #     newGame = Games()
        #     newGame.gameID = newGameID
        # newGame.gameLun = lun + 1
        #
        # newGame.gameNum = math.floor(num / 2)
        # newGame.gameServer = server
        # if num % 2 == 0:
        #     newGame.gamePlayer1ID = winner
        #     newGame.gamePlayer2ID = ''
        # else:
        #     newGame.gamePlayer1ID = ''
        #     newGame.gamePlayer2ID = winner
        # newGame.gameResult = winner
        # newGame.save()
        return 1
    return 1

def updateXZSGame(server, gameID, winner, score):
    try:
        game = Games.objects.get(gameServer=server,
                                 gameID=gameID,
                                 gameType=1
                                 )
    except:
        return -11
    try:
        player1 = fightPlayer.objects.get(playerServer=server,
                                         playerID=winner
                                         )
    except:
        return -12
    #print(player1.playerScore)
    #print(score)

    if not(cmp(game.gamePlayer2ID, winner)==0 or cmp(game.gamePlayer1ID, winner)==0):
        return -17
    if len(game.gameResult)>0:
        return -18



    game.gameResult = winner
    game.gameScore = score
    game.save()
    oscore = int(player1.playerScore)
    player1.playerScore = int(oscore + score)
    player1.save()
    lun = game.gameLun

    try:
        games = Games.objects.filter(gameServer=server,
                                     gameLun=lun,
                                     gameType = 1)
    except:
        return -13

    flag = True

    for g in games:
        if len(g.gameResult) == 0:
            flag = False

    if flag:
        try:
            players = fightPlayer.objects.filter(playerServer = server, playerNowState = lun).order_by('-playerScore')
        except:
            return -14

        for i in range(4, len(players)):
            player = players[i]
            player.playerServer = player.playerServer + '-'
            player.save()
        try:
            players = fightPlayer.objects.filter(playerServer = server)
        except:
            return -15
        if len(players) == 16:
            try:
                players1 = fightPlayer.objects.filter(playerServer=server, playerNowState=0).order_by('-playerScore','gameTime')
                players2 = fightPlayer.objects.filter(playerServer=server, playerNowState=1).order_by('-playerScore','gameTime')
                players3 = fightPlayer.objects.filter(playerServer=server, playerNowState=2).order_by('-playerScore','gameTime')
                players4 = fightPlayer.objects.filter(playerServer=server, playerNowState=3).order_by('-playerScore','gameTime')
            except:
                return -16
            players = [players1, players2, players3, players4]
            cd1 = [2,2,3,3]
            cd2 = [[2,3],[2,3]]
            random.shuffle(cd1)
            random.shuffle(cd2[0])
            random.shuffle(cd2[1])
            ab1 = [0, 0, 1, 1]
            ab2 = [[0, 0], [1, 1]]
            random.shuffle(ab1)
            random.shuffle(ab2[0])
            random.shuffle(ab2[1])
            guize = [[0, 0],
                     [cd1[0], cd2[cd1[0]-2][0]],
                     [1, 1],
                     [cd1[1], cd2[cd1[1]-2][1]],
                     [2, 0],
                     [ab1[0], ab2[ab1[0]][0]],
                     [3, 1],
                     [ab1[1], ab2[ab1[1]][1]],
                     [0, 1],
                     [cd1[2], cd2[cd1[2]-2][0]],
                     [1, 0],
                     [cd1[3], cd2[cd1[3]-2][1]],
                     [2, 1],
                     [ab1[2], ab2[ab1[2]][0]],
                     [3, 0],
                     [ab1[3], ab2[ab1[3]][1]]]
            for i in range(int(len(guize)/2)):
                game = Games()
                game.gameID = server + str(0) + str(0) + str(i)
                game.gameLun = 0
                game.gameNum = i
                game.gameServer = server
                game.gamePlayer1ID = players[guize[i*2][0]][guize[i*2][1]].playerID
                game.gamePlayer2ID = players[guize[i*2+1][0]][guize[i*2+1][1]].playerID
                game.save()
    return 1

def getGameList(server):
    try:
        games = Games.objects.filter(gameServer=server,
                                     gameType=0)
        if len(games)==0:
            games = Games.objects.filter(gameServer=server,
                                         gameType=1)
            gameType = 1
        else:
            gameType = 0
    except:
            return ''
    gameList = []
    for game in games:
        gameInfo = {}
        gameInfo['gameId'] = game.gameID
        gameInfo['player1'] = game.gamePlayer1ID
        gameInfo['player2'] = game.gamePlayer2ID
        gameInfo['gameLun'] = game.gameLun
        gameInfo['gameNum'] = game.gameNum
        gameInfo['gameResult'] = game.gameResult
        gameInfo['gameScore'] = game.gameScore
        gameList.append(gameInfo)
    return json.dumps({'gameType':gameType,'gameList':gameList},encoding='utf8',ensure_ascii=False)
