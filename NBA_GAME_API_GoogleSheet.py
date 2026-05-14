from datetime import datetime

# 獲取當前年份與月份
now = datetime.now()
current_year = now.year
current_month = now.month

# 判斷賽季
# 如果是 8 月(含)之後，賽季為 "今年-明年"
# 如果是 7 月(含)之前，賽季為 "去年-今年"
if current_month >= 8:
    season = f"{current_year}-{str(current_year + 1)[-2:]}"
else:
    season = f"{current_year - 1}-{str(current_year)[-2:]}"

from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.endpoints import leaguestandings
from nba_api.live.nba.endpoints import scoreboard
import pandas as pd

# 定義偽裝成一般瀏覽器的 Headers
custom_headers = {
    'Host': 'cdn.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
    'If-Modified-Since': 'Sat, 01 Jan 2024 00:00:00 GMT' # 有時候加這個能避開快取阻擋
}

games = scoreboard.ScoreBoard(headers=custom_headers)
games_dict = games.get_dict()['scoreboard']['games']
'''
finalFlag  0:全部    1:只看進行中的
shortView  0:Detail  1:Master
'''
finalFlag = 0
shortView = 0
gameIDList = []
if shortView==0:
    for i in games_dict:
        if finalFlag==1 and i['gameStatusText'][:5]=='Final':
            pass
        else:
            # print(i['gameId'])
            gameIDList.append(i['gameId'])
            # print(i['homeTeam']['teamName']+' '+i['homeTeam']['teamCity']+' '+i['homeTeam']['teamTricode']+'    '+str(i['homeTeam']['score']))
            # if len(i['homeTeam']['periods'])==4:
                # print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score']))
                # print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                # print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score']))
            # elif len(i['homeTeam']['periods'])==5:
                # print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score'])+' '+str(i['homeTeam']['periods'][4]['score']))
                # print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                # print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score'])+' '+str(i['awayTeam']['periods'][4]['score']))
            # else:
                # print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score'])+' '+str(i['homeTeam']['periods'][4]['score'])+' '+str(i['homeTeam']['periods'][5]['score']))
                # print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                # print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score'])+' '+str(i['awayTeam']['periods'][4]['score'])+' '+str(i['awayTeam']['periods'][5]['score']))
            # print(i['gameStatusText'])
            # print('------------------------------------------')
# else:
    # for i in games_dict:
        # if i['gameStatusText'].rstrip()=='Half':
            # print(i['gameStatusText'].rstrip()+'      '+i['homeTeam']['teamTricode']+' - '+i['awayTeam']['teamTricode']+'   '+str(i['homeTeam']['score'])+' - '+str(i['awayTeam']['score']))
        # else:
            # print(i['gameStatusText'].rstrip()+'   '+i['homeTeam']['teamTricode']+' - '+i['awayTeam']['teamTricode']+'   '+str(i['homeTeam']['score'])+' - '+str(i['awayTeam']['score']))

from nba_api.live.nba.endpoints import BoxScore
import numpy as np

li = [['team','num','name','min','pts','ass','reb','stl','blk','to','foul','%','2%','3%','3#','3#/','2#','2#/','1#','1#/','EFF']]
for gameID in gameIDList:

    box = BoxScore(gameID, headers=custom_headers)
    box_dict = box.get_dict()
    
    awayTeam = box_dict['game']['awayTeam']['players']
    homeTeam = box_dict['game']['homeTeam']['players']
    
    for i in awayTeam:
        if i['statistics']['minus']==0:
            pass
        else:
            temp = []
            temp.append(box_dict['game']['awayTeam']['teamTricode'])
            temp.append(i['jerseyNum'])
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
            temp.append(i['jerseyNum'])
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

if len(gameIDList)>0:
    nba_gameDataDF = pd.DataFrame(np.array(li[1:]),columns=np.array(li[0]))
    nba_gameDataDF = nba_gameDataDF.astype({'pts': 'int64','ass': 'int64','reb': 'int64','stl': 'int64','blk': 'int64',
                            'to': 'int64','foul': 'int64','%': 'float64','2%': 'float64','3%': 'float64',
                            '3#':'int64','3#/':'int64','2#':'int64','2#/':'int64','1#':'int64','1#/':'int64','EFF':'float64'})
    
    import os
    
    # --- 1. 準備資料 ---
    # 新增執行日期欄位
    current_date = datetime.now().strftime('%Y/%m/%d')
    nba_gameDataDF.insert(0, 'EXECUTION_DATE', current_date)
    
    # 定義檔名
    file_name = f"NBA_Players_PerGame_{season}.csv"
    
    # --- 2. 判斷檔案是否存在並寫入 ---
    if not os.path.exists(file_name):
        # 如果檔案不存在：新建檔案，寫入標題列 (header=True)
        nba_gameDataDF.to_csv(file_name, index=True, encoding='utf-8-sig')
        print(f"🆕 檔案不存在，已建立新檔: {file_name}")
    else:
        # 如果檔案已存在：附加在最後面 (mode='a')，且不重複寫入標題 (header=False)
        nba_gameDataDF.to_csv(file_name, mode='a', index=True, header=False, encoding='utf-8-sig')
        print(f"📝 檔案已存在，已將資料附加至: {file_name}")
