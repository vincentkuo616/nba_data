from datetime import datetime
import os
import sys  # ◄── 新增引入系統模組，用於優雅退出
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.endpoints import leaguestandings
import pandas as pd

# 獲取當前年份與月份
now = datetime.now()
current_year = now.year
current_month = now.month

# ==============================================================================
# 🛡️ 核心強化：季節防禦閘門 (僅在 10/1 ~ 4/30 執行)
# 10/1 到次年 4/30 代表月份必須是 10, 11, 12月 或是 1, 2, 3, 4月
# ==============================================================================
if not (current_month >= 10 or current_month <= 4):
    print(
        f"📢 目前月份為 {current_month} 月（非賽季期間 10/1 ~ 4/30）。"
    )
    print("💡 系統啟動防禦機制：自動跳過本次執行，優雅退出。")
    sys.exit(
        0
    )  # 回傳 0 代表正常結束，確保 GitHub Actions / Pipeline 依然保持綠燈成功狀態

print("🏀 進入賽季限定期間，開始執行 NBA 數據撈取任務...")

# ==============================================================================
# 📊 以下維持你原本的精美資料處理邏輯
# ==============================================================================

# 判斷賽季
# 如果是 8 月(含)之後，賽季為 "今年-明年"
# 如果是 7 月(含)之前，賽季為 "去年-今年"
if current_month >= 8:
    season = f"{current_year}-{str(current_year + 1)[-2:]}"
else:
    season = f"{current_year - 1}-{str(current_year)[-2:]}"

season_type = "Regular Season"  # --Playoffs  Regular Season  All Star
nba_players = leagueleaders.LeagueLeaders(
    season=season,
    season_type_all_star=season_type,  # --Playoffs  Regular Season  All Star
    stat_category_abbreviation="PTS",
).get_data_frames()[0][:]

# Group players by name and player ID and calculate average stats
nba_players_avg = nba_players.groupby(["PLAYER", "PLAYER_ID", "TEAM"]).mean()[[
    "MIN",
    "FGM",
    "FGA",
    "FTM",
    "FTA",
    "PTS",
    "FG3M",
    "FG3A",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "EFF",
    "AST_TOV",
    "STL_TOV",
    "GP",
]]

nba_players_avg["A_PTS"] = nba_players_avg["PTS"] / nba_players_avg["GP"]
nba_players_avg["A_OREB"] = nba_players_avg["OREB"] / nba_players_avg["GP"]
nba_players_avg["A_DREB"] = nba_players_avg["DREB"] / nba_players_avg["GP"]
nba_players_avg["A_REB"] = nba_players_avg["REB"] / nba_players_avg["GP"]
nba_players_avg["A_AST"] = nba_players_avg["AST"] / nba_players_avg["GP"]
nba_players_avg["A_STL"] = nba_players_avg["STL"] / nba_players_avg["GP"]
nba_players_avg["A_BLK"] = nba_players_avg["BLK"] / nba_players_avg["GP"]
nba_players_avg["A_TOV"] = nba_players_avg["TOV"] / nba_players_avg["GP"]
nba_players_avg["A_PF"] = nba_players_avg["PF"] / nba_players_avg["GP"]
nba_players_avg["A_EFF"] = nba_players_avg["EFF"] / nba_players_avg["GP"]
nba_players_avg["3_%"] = nba_players_avg["FG3M"] / nba_players_avg["FG3A"]
nba_players_avg["FG_%"] = nba_players_avg["FGM"] / nba_players_avg["FGA"]
nba_players_avg["FT_%"] = nba_players_avg["FTM"] / nba_players_avg["FTA"]
nba_players_avg["A_3"] = nba_players_avg["FG3A"] / nba_players_avg["GP"]
nba_players_avg["A_FGA"] = nba_players_avg["FGA"] / nba_players_avg["GP"]
nba_players_avg["A_FTA"] = nba_players_avg["FTA"] / nba_players_avg["GP"]
nba_players_avg["A_MIN"] = nba_players_avg["MIN"] / nba_players_avg["GP"]
nba_players_avg["FG2A"] = nba_players_avg["FGA"] - nba_players_avg["FG3A"]
nba_players_avg["FG2M"] = nba_players_avg["FGM"] - nba_players_avg["FG3M"]
nba_players_avg["2_%"] = nba_players_avg["FG2M"] / nba_players_avg["FG2A"]
nba_players_avg["A_2"] = nba_players_avg["FG2A"] / nba_players_avg["GP"]
nba_players_avg = nba_players_avg[[
    "GP",
    "A_MIN",
    "A_FGA",
    "FG_%",
    "A_3",
    "3_%",
    "A_2",
    "2_%",
    "A_FTA",
    "FT_%",
    "A_PTS",
    "A_REB",
    "A_OREB",
    "A_DREB",
    "A_AST",
    "A_STL",
    "A_BLK",
    "A_TOV",
    "A_PF",
    "A_EFF",
    "AST_TOV",
    "STL_TOV",
    "MIN",
    "FGM",
    "FGA",
    "FG3M",
    "FG3A",
    "FG2M",
    "FG2A",
    "FTM",
    "FTA",
    "PTS",
    "REB",
    "OREB",
    "DREB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "EFF",
]]

# 完整顯示所有欄位
pd.set_option("display.max_columns", None)
# 改變浮點數顯示位數
pd.set_option("display.precision", 1)

# --- 1. 準備資料 ---
# 新增執行日期欄位
current_date = datetime.now().strftime("%Y/%m/%d")
nba_players_avg.insert(0, 'EXECUTION_DATE', current_date)

# 定義檔名
file_name = f"NBA_Players_{season}.csv"

# --- 2. 判斷檔案是否存在並寫入 ---
if not os.path.exists(file_name):
    # 如果檔案不存在：新建檔案，寫入標題列 (header=True)
    nba_players_avg.to_csv(file_name, index=True, encoding="utf-8-sig")
    print(f"🆕 檔案不存在，已建立新檔: {file_name}")
else:
    # 如果檔案已存在：附加在最後面 (mode='a')，且不重複寫入標題 (header=False)
    nba_players_avg.to_csv(
        file_name, mode="a", index=True, header=False, encoding="utf-8-sig"
    )
    print(f"📝 檔案已存在，已將資料附加至: {file_name}")
