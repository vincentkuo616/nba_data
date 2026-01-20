from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.endpoints import leaguestandings
from nba_api.live.nba.endpoints import scoreboard
import pandas as pd

# Pull data for the top 500 scorers by PTS column
season = '2025-26'
season_type = 'Regular Season' #--Playoffs  Regular Season  All Star
nba_players = leagueleaders.LeagueLeaders(
    season=season, #--2023-24
    season_type_all_star=season_type, #--Playoffs  Regular Season  All Star
    stat_category_abbreviation='PTS'
).get_data_frames()[0][:]

# Group players by name and player ID and calculate average stats
nba_players_avg = nba_players.groupby(['PLAYER', 'PLAYER_ID', 'TEAM']).mean()[[
    'MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'PTS', 'FG3M', 'FG3A', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'EFF', 'AST_TOV', 'STL_TOV', 'GP'
]]

nba_players_avg['A_PTS']=nba_players_avg['PTS']/nba_players_avg['GP']
nba_players_avg['A_OREB']=nba_players_avg['OREB']/nba_players_avg['GP']
nba_players_avg['A_DREB']=nba_players_avg['DREB']/nba_players_avg['GP']
nba_players_avg['A_REB']=nba_players_avg['REB']/nba_players_avg['GP']
nba_players_avg['A_AST']=nba_players_avg['AST']/nba_players_avg['GP']
nba_players_avg['A_STL']=nba_players_avg['STL']/nba_players_avg['GP']
nba_players_avg['A_BLK']=nba_players_avg['BLK']/nba_players_avg['GP']
nba_players_avg['A_TOV']=nba_players_avg['TOV']/nba_players_avg['GP']
nba_players_avg['A_PF']=nba_players_avg['PF']/nba_players_avg['GP']
nba_players_avg['A_EFF']=nba_players_avg['EFF']/nba_players_avg['GP']
nba_players_avg['3_%']=nba_players_avg['FG3M']/nba_players_avg['FG3A']
nba_players_avg['FG_%']=nba_players_avg['FGM']/nba_players_avg['FGA']
nba_players_avg['FT_%']=nba_players_avg['FTM']/nba_players_avg['FTA']
nba_players_avg['A_3']=nba_players_avg['FG3A']/nba_players_avg['GP']
nba_players_avg['A_FGA']=nba_players_avg['FGA']/nba_players_avg['GP']
nba_players_avg['A_FTA']=nba_players_avg['FTA']/nba_players_avg['GP']
nba_players_avg['A_MIN']=nba_players_avg['MIN']/nba_players_avg['GP']
nba_players_avg['FG2A']=nba_players_avg['FGA']-nba_players_avg['FG3A']
nba_players_avg['FG2M']=nba_players_avg['FGM']-nba_players_avg['FG3M']
nba_players_avg['2_%']=nba_players_avg['FG2M']/nba_players_avg['FG2A']
nba_players_avg['A_2']=nba_players_avg['FG2A']/nba_players_avg['GP']
nba_players_avg = nba_players_avg[['GP','A_MIN','A_FGA','FG_%','A_3','3_%','A_2','2_%','A_FTA','FT_%','A_PTS','A_REB','A_OREB','A_DREB','A_AST','A_STL','A_BLK','A_TOV','A_PF','A_EFF','AST_TOV','STL_TOV','MIN','FGM','FGA','FG3M','FG3A','FG2M','FG2A','FTM','FTA','PTS','REB','OREB','DREB','AST','STL','BLK','TOV','PF','EFF']]

# 完整顯示所有欄位
pd.set_option("display.max_columns", None)
# 改變浮點數顯示位數
pd.set_option("display.precision", 1)

from datetime import datetime
import os

# --- 1. 準備資料 ---
# 新增執行日期欄位
current_date = datetime.now().strftime('%Y/%m/%d')
nba_players_avg.insert(0, 'EXECUTION_DATE', current_date)

# 定義檔名
file_name = f"NBA_Players_{season}.csv"

# --- 2. 判斷檔案是否存在並寫入 ---
if not os.path.exists(file_name):
    # 如果檔案不存在：新建檔案，寫入標題列 (header=True)
    nba_players_avg.to_csv(file_name, index=True, encoding='utf-8-sig')
    print(f"🆕 檔案不存在，已建立新檔: {file_name}")
else:
    # 如果檔案已存在：附加在最後面 (mode='a')，且不重複寫入標題 (header=False)
    nba_players_avg.to_csv(file_name, mode='a', index=True, header=False, encoding='utf-8-sig')
    print(f"📝 檔案已存在，已將資料附加至: {file_name}")
