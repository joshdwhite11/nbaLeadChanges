import requests as r
import pandas as pd
import pprint
import time
import itertools
from nba_api.stats.endpoints import boxscoresummaryv2, leaguegamefinder

pp = pprint.PrettyPrinter(indent = 4)
lastTenYears = ["2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]
gameidlistpre = []

for i in lastTenYears:
    gamefinder = leaguegamefinder.LeagueGameFinder(season_type_nullable = "Playoffs", season_nullable = i, league_id_nullable = "00").get_data_frames()[0]["GAME_ID"]
    gameidlistpre.append(list(set(list(gamefinder))))

gameidlist = list(itertools.chain(*gameidlistpre))
gameidlist.sort()
#print(gameidlist)

masterdf = pd.DataFrame(columns = ["GAME_ID", "LEAD_CHANGES", "TEAM_ABBRV", "GAME_DATE"])
counter = 0

print(len(gameidlist))
time.sleep(60)

for i in gameidlist:
    lead_changes = list(boxscoresummaryv2.BoxScoreSummaryV2(i).other_stats.get_data_frame()[["LEAD_CHANGES", "TEAM_ABBREVIATION"]].iloc[0,:])
    lead_changes_date = list(boxscoresummaryv2.BoxScoreSummaryV2(i).game_info.get_data_frame()["GAME_DATE"])
    masterlist = [0,0,0,0]
    masterlist[0] = i
    masterlist[1] = lead_changes[0]
    masterlist[2] = lead_changes[1]
    masterlist[3] = lead_changes_date[0]

    masterdf.loc[counter] = masterlist
    print(masterdf)
    counter += 1
    time.sleep(60)

masterdf.to_csv("nbaleadchange.csv")
