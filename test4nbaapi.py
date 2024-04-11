# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:57:01 2023

@author: vincentkuo
"""

from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.endpoints import leaguestandings
from nba_api.live.nba.endpoints import scoreboard
import pandas as pd

# Pull data for the top 500 scorers by PTS column
nba_players = leagueleaders.LeagueLeaders(
    season='2023-24',
    season_type_all_star='Regular Season',
    stat_category_abbreviation='PTS'
).get_data_frames()[0][:]

# Group players by name and player ID and calculate average stats
nba_players_avg = nba_players.groupby(['PLAYER', 'PLAYER_ID', 'TEAM']).mean()[[
    'MIN', 'FGM', 'FGA', 'FTM', 'FTA', 'PTS', 'FG3M', 'FG3A', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'EFF', 'AST_TOV', 'STL_TOV', 'GP'
]]


#print(top_500_avg)

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



# Team INFORMATION
nba_teams = leaguestandings.LeagueStandings(season='2023-24').get_data_frames()[0][:]
#print(teams)

games = scoreboard.ScoreBoard()
games_dict = games.get_dict()['scoreboard']['games']
'''
finalFlag  0:全部    1:只看進行中的
shortView  0:Detail  1:Master
'''
finalFlag = 0
shortView = 0
if shortView==0:
    for i in games_dict:
        if finalFlag==1 and i['gameStatusText'][:5]=='Final':
            pass
        else:
            print(i['gameId'])
            print(i['homeTeam']['teamName']+' '+i['homeTeam']['teamCity']+' '+i['homeTeam']['teamTricode']+'    '+str(i['homeTeam']['score']))
            if len(i['homeTeam']['periods'])==4:
                print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score']))
                print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score']))
            elif len(i['homeTeam']['periods'])==5:
                print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score'])+' '+str(i['homeTeam']['periods'][4]['score']))
                print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score'])+' '+str(i['awayTeam']['periods'][4]['score']))
            else:
                print(str(i['homeTeam']['periods'][0]['score'])+' '+str(i['homeTeam']['periods'][1]['score'])+' '+str(i['homeTeam']['periods'][2]['score'])+' '+str(i['homeTeam']['periods'][3]['score'])+' '+str(i['homeTeam']['periods'][4]['score'])+' '+str(i['homeTeam']['periods'][5]['score']))
                print(i['awayTeam']['teamName']+' '+i['awayTeam']['teamCity']+' '+i['awayTeam']['teamTricode']+'    '+str(i['awayTeam']['score']))
                print(str(i['awayTeam']['periods'][0]['score'])+' '+str(i['awayTeam']['periods'][1]['score'])+' '+str(i['awayTeam']['periods'][2]['score'])+' '+str(i['awayTeam']['periods'][3]['score'])+' '+str(i['awayTeam']['periods'][4]['score'])+' '+str(i['awayTeam']['periods'][5]['score']))
            print(i['gameStatusText'])
            print('------------------------------------------')
else:
    for i in games_dict:
        if i['gameStatusText'].rstrip()=='Half':
            print(i['gameStatusText'].rstrip()+'      '+i['homeTeam']['teamTricode']+' - '+i['awayTeam']['teamTricode']+'   '+str(i['homeTeam']['score'])+' - '+str(i['awayTeam']['score']))
        else:
            print(i['gameStatusText'].rstrip()+'   '+i['homeTeam']['teamTricode']+' - '+i['awayTeam']['teamTricode']+'   '+str(i['homeTeam']['score'])+' - '+str(i['awayTeam']['score']))

def findID(name, team_name):
    from nba_api.stats.static import players, teams
    
    nba_players = players.get_players()
    nba_teams = teams.get_teams()
    # print(nba_players)
    # name = 'LeBron James' # 2544 1610612747
    playerID,teamID="",""
    for player in nba_players:
        if player['full_name']==name:
            playerID = player['id']
    for team in nba_teams:
        if team['abbreviation']==team_name:
            teamID = team['id']
            return playerID, teamID
    return False

import matplotlib as mpl
import matplotlib.pyplot as plt

def create_Court(ax: mpl.axes, color='white') -> mpl.axes:
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-250, 250], [0, 0], linewidth=4, color='black')
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    return ax

def shot_chart(df: pd.DataFrame, name: str, season=None, RA=True, extent=(-250, 250, 422.5, -47.5), gridsize=25, cmap='Reds'):
    fig = plt.figure(figsize=(3.6, 3.6), facecolor='white', edgecolor='white', dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], facecolor='white')
    ax = create_Court(ax)
    
    # Plot hexbin of shots
    if RA==True:
        x = df.LOC_X
        y = df.LOC_Y + 60
        # Annotate player name and season
        plt.text(-240, 430, f"{name}", fontsize=21, color='black')
        season = f"NBA {season[0][:4]}-{season[-1][-2:]}"
        plt.scatter(x, y, marker='H', alpha=0.5, cmap='Reds')
    else:
        x = df.LOC_X
        y = df.LOC_Y
        plt.scatter(x, y, marker='H', c='Red' , alpha=0.5, cmap='BrBG')

from nba_api.stats.endpoints import shotchartdetail
# Dirk Nowitzki 1717 1610612742 2010-11 Ray Allen Jeremy Lin
# LeBron James  2544 1610612747 1610612748 Luka Doncic Kyrie Irving Joel Embiid Nikola Jokic Pascal Siakam
# Shai Gilgeous-Alexander DeMar DeRozan Alex Caruso Ben Simmons Seth Curry Kyle Korver 436 x 119 x 19  460g
name = 'Kyle Korver'
seasons = '2019-20'
team = 'MIL'
player_id, team_id = findID(name,team)
scd = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id, season_nullable=seasons)
df2 = scd.get_data_frames()[0]

#chart2 = shot_chart(df2, name, seasons, RA=False)

#plt.show()

from nba_api.stats.endpoints import TeamGameLogs

gamedatapull = TeamGameLogs(
            league_id_nullable = '00', # nba 00, g_league 20, wnba 10
            team_id_nullable = '', # can specify a specific team_id
            season_nullable = '2023-24',
            season_type_nullable = 'Regular Season' # Regular Season, Playoffs, Pre Season
        )

df_season = gamedatapull.get_data_frames()[0]
