# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 09:26:20 2023

@author: vincentkuo
"""

from nba_api.stats.endpoints import leagueleaders
from nba_api.live.nba.endpoints import scoreboard, BoxScore
import pandas as pd
import numpy as np

gameIDList = ['0022301201','0022301203']
gameIDList = [] # 25 ~ 38
for i in range(7):
    gameIDList.append('00'+str(i+22300946)) # 304 13  69
#    if i == 3:  gameIDList.pop()
#gameIDList.append('00'+str(22300576))
#gameIDList = ['0032300001']

li = [['team','name','min','pts','ass','reb','stl','blk','to','foul','%','2%','3%','3#','3#/','2#','2#/','1#','1#/','EFF']]
for gameID in gameIDList:

    box = BoxScore(gameID)
    box_dict = box.get_dict()
    
    #print(box_dict['game']['awayTeam']['players'][0])
    
    awayTeam = box_dict['game']['awayTeam']['players']
    homeTeam = box_dict['game']['homeTeam']['players']
    
    for i in awayTeam:
        if i['statistics']['minus']==0:
            pass
        else:
            temp = []
            temp.append(box_dict['game']['awayTeam']['teamTricode'])
            temp.append(i['name'])
            temp.append(i['statistics']['minutes'])
            temp.append(i['statistics']['points'])
            temp.append(i['statistics']['assists'])
            temp.append(i['statistics']['reboundsTotal'])
            temp.append(i['statistics']['steals'])
            temp.append(i['statistics']['blocks'])
            temp.append(i['statistics']['turnovers'])
            temp.append(i['statistics']['foulsPersonal'])
            temp.append(i['statistics']['fieldGoalsPercentage'])
            temp.append(i['statistics']['twoPointersPercentage'])
            temp.append(i['statistics']['threePointersPercentage'])
            temp.append(i['statistics']['threePointersMade'])
            temp.append(i['statistics']['threePointersAttempted'])
            temp.append(i['statistics']['twoPointersMade'])
            temp.append(i['statistics']['twoPointersAttempted'])
            temp.append(i['statistics']['freeThrowsMade'])
            temp.append(i['statistics']['freeThrowsAttempted'])
            temp.append(i['statistics']['plusMinusPoints'])
            li.append(temp)
    for i in homeTeam:
        if i['statistics']['minus']==0:
            pass
        else:
            temp = []
            temp.append(box_dict['game']['homeTeam']['teamTricode'])
            temp.append(i['name'])
            temp.append(i['statistics']['minutes'])
            temp.append(i['statistics']['points'])
            temp.append(i['statistics']['assists'])
            temp.append(i['statistics']['reboundsTotal'])
            temp.append(i['statistics']['steals'])
            temp.append(i['statistics']['blocks'])
            temp.append(i['statistics']['turnovers'])
            temp.append(i['statistics']['foulsPersonal'])
            temp.append(i['statistics']['fieldGoalsPercentage'])
            temp.append(i['statistics']['twoPointersPercentage'])
            temp.append(i['statistics']['threePointersPercentage'])
            temp.append(i['statistics']['threePointersMade'])
            temp.append(i['statistics']['threePointersAttempted'])
            temp.append(i['statistics']['twoPointersMade'])
            temp.append(i['statistics']['twoPointersAttempted'])
            temp.append(i['statistics']['freeThrowsMade'])
            temp.append(i['statistics']['freeThrowsAttempted'])
            temp.append(i['statistics']['plusMinusPoints'])
            li.append(temp)
    
teamDF = pd.DataFrame(np.array(li[1:]),columns=np.array(li[0]))
teamDF = teamDF.astype({'pts': 'int64','ass': 'int64','reb': 'int64','stl': 'int64','blk': 'int64',
                        'to': 'int64','foul': 'int64','%': 'float64','2%': 'float64','3%': 'float64',
                        '3#':'int64','3#/':'int64','2#':'int64','2#/':'int64','1#':'int64','1#/':'int64','EFF':'float64'})
#print(teamDF)