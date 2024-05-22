from SportsInfoAPI import MLB
import SportsInfoAPI
import time
# Test cases for get_player_id, Returns Babe Ruth Babeball Reference ID
start_time = time.time()
print(MLB.get_player_id("Ruth", "Babe",bbref=True))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_player_id, Returns all of Lou Gehrig Ids
start_time = time.time()
print(MLB.get_player_id("Gehrig", "Lou"))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for all_time_leaders, Returns the all time home run leaders
start_time = time.time()
print(MLB.all_time_leaders("home runs"))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_mvps
#Returns the 2023 MVPs
start_time = time.time()
print(MLB.get_mvps(year=2023))
print(f"Execution time: {time.time() - start_time} seconds\n")

#Returns the 2021 American League MVP
start_time = time.time()
print(MLB.get_mvps(year=2021, AL=True))
print(f"Execution time: {time.time() - start_time} seconds\n")

#Returns the 2022 National League MVP
start_time = time.time()
print(MLB.get_mvps(year=2022, NL=True))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_best_record in the year selected
start_time = time.time()
print(MLB.get_best_record(date=2024))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_team_results,Returns the winner of the phillies game on April 22 2023
start_time = time.time()
team=SportsInfoAPI.get_team_names(nickname='phillies')
date=SportsInfoAPI.date_convertion('04/22/2023')
#print(MLB.get_team_results(team,int(date[1]),date[0],winner=True,date=date))
#print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_world_series_winner in the year selected
start_time = time.time()
print(MLB.get_world_series_winner(year=2023))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_home_team_wins, for the yankees in the year selected
start_time = time.time()
print(MLB.get_home_team_wins(requested_season=2023,requested_team='NYA'))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_extra_inning_walkoffs for the yankees in 2023
start_time = time.time()
print(MLB.get_extra_inning_walkoffs("NYA", requested_year=2023))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_high_scoring_games where the dodgers scored 10 runs
start_time = time.time()
print(MLB.get_high_scoring_games("LAN", 10,2022))
print(f"Execution time: {time.time() - start_time} seconds\n")


# Test cases for get_games_with_many_pitchers where the san fransico giants used 5 pitchers
start_time = time.time()
print(MLB.get_games_with_many_pitchers("SFN", 5, requested_year=2023))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_umpire_with_most_runs, returns the umpire who was the home plate ump for the most runs scored
start_time = time.time()
print(MLB.get_umpire_with_most_runs(requested_season=2023))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_day_night_wins, get the number of day game wins for the yankees in 2023
start_time = time.time()
print(MLB.get_day_night_wins(2023,'NYA',day=True))
print(f"Execution time: {time.time() - start_time} seconds\n")

# Test cases for get_winning_streak, longest winning streak for a team in 2023
start_time = time.time()
team=SportsInfoAPI.get_team_names(RetroName='yankees',retro=True)
MLB.get_winning_streak(requested_team=team)
print(f"Execution time: {time.time() - start_time} seconds\n")
