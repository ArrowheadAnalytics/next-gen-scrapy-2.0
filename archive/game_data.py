import numpy as np
import nflgame
import pandas as pd
games = nflgame.games(2019)

game_stat = []
for game in games:
    game_stat.append([game.eid,game.season(),game.home,game.away])
    
game_df = pd.DataFrame(game_stat,columns = ['game_id','season','home_team','away_team'])
game_df.game_id = game_df.game_id.astype(int)
pass_location = pd.read_csv('pass_locations.csv')

pass_and_game_data = pd.merge(pass_location,game_df,on='game_id')
pass_and_game_data['type'] = pass_and_game_data.week.apply(lambda x: 'reg' if str(x).isdigit() else 'post')

teams = ["arizona-cardinals",
	"atlanta-falcons",
	"baltimore-ravens",
	"buffalo-bills",
	"carolina-panthers",
	"chicago-bears",
	"cincinnati-bengals",
	"cleveland-browns",
	"dallas-cowboys",
	"denver-broncos",
	"detroit-lions",
	"green-bay-packers",
	"houston-texans",
	"indianapolis-colts",
	"jacksonville-jaguars",
	"kansas-city-chiefs",
	"los-angeles-chargers",
	"los-angeles-rams",
	"miami-dolphins",
	"minnesota-vikings",
	"new-england-patriots",
	"new-orleans-saints",
	"new-york-giants",
	"new-york-jets",
	"oakland-raiders",
	"philadelphia-eagles",
	"pittsburgh-steelers",
	"san-francisco-49ers",
	"seattle-seahawks",
	"tampabay-buccaneers",
	"tennessee-titans",
	"washington-redskins"
]


team_abbv = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL',
       'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LA', 'MIA',
       'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SEA', 'SF',
       'TB', 'TEN', 'WAS']

pass_and_game_data['team'] = pass_and_game_data['team'].replace(teams,team_abbv)
pass_and_game_data['home_team'] = pass_and_game_data['home_team'].replace(teams,team_abbv)
pass_and_game_data['away_team'] = pass_and_game_data['away_team'].replace(teams,team_abbv)

pass_and_game_data.to_csv("./pass_and_game_data.csv")
