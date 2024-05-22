from SportsInfoAPI import NBA
import time

# Test case for get_mvp function: Gets the NBA MVP for 2023
start_time = time.time()
print(NBA.get_mvp(2023, 0))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_nba_championship_winner function, Returns the Champinons of the 2023 Season
start_time = time.time()
print(NBA.get_nba_championship_winner(2023, 0))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_player_award function, Finds all the times that Lebron James has won All_NBA
start_time = time.time()
print(NBA.get_player_award("2544", "All-NBA"))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for single_game_records function, Currently only returns the record for most points scored in a game
start_time = time.time()
print(NBA.single_game_records())
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for league_leaders function, Returns the leaders in rebounds this season
start_time = time.time()
print(NBA.league_leaders(20))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_NBA_team_details function, Returns details about the los angeles lakers
start_time = time.time()
print(NBA.get_NBA_team_details("1610612747")) # Los Angeles Lakers
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_nba_career_stats function, Returns the carer stats for lebron James
start_time = time.time()
print(NBA.get_nba_career_stats("2544")) # LeBron James
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_career_averages function, Returns lebron james career averages
start_time = time.time()
print(NBA.get_career_averages("2544")) # LeBron James
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_player_game_logs function, returns every game that lebron had a triple double in 2022
start_time = time.time()
print(NBA.get_player_game_logs("2544", 2022,TD=True)) # LeBron James
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_NBA_team_roster function, returns the current san antonio spurs rosters
start_time = time.time()
id=NBA.get_team_id('Spurs')
print(NBA.get_NBA_team_roster(id))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for AllTimeLeaders function, returns the all time leader in points 
start_time = time.time()
print(NBA.AllTimeLeaders())
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_team_schedule function, returns the lakers schedule from 2023
start_time = time.time()
print(NBA.get_team_schedule("1610612747")) # Los Angeles Lakers
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test case for get_league_standings function, returns the current nba standings.
start_time = time.time()
print(NBA.get_league_standings(2023, 0))
print(f"Execution time: {time.time() - start_time} seconds\n")


