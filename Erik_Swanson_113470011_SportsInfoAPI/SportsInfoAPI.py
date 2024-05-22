class NBA:
    def __init__(self):
        import nltk
        pass
    # --Each of these are using the NBA API
    def get_player_ID_NBA(last_name: str, first_name: str) -> dict:
        """
        This function retrieves the NBA player ID for a given player's first and last name.

        Parameters:
        last_name (str): The last name of the NBA player.
        first_name (str): The first name of the NBA player.

        Returns:
        dict: A dictionary containing the player's ID if the player is found. 
          If the player is not found, it prints "Player not found." and returns None.

        Example:
        get_player_ID_NBA('James', 'LeBron')
        2544
        """
        from nba_api.stats.static import players
        nba_players = players.get_players()
        first_name = first_name.lower()
        last_name = last_name.lower()
        Theplayer = [player for player in nba_players if player['first_name'].lower() == first_name and player['last_name'].lower() == last_name]
        if Theplayer:
            return Theplayer[0]['id']
        else:
            print("Player not found.")
            return None
    
    def get_mvp(year,league=0):
        """
    Fetches the Most Valuable Player (MVP) of a given year from the basketball-reference website.

    This function sends a GET request to the basketball-reference website, parses the HTML response to extract the MVP tables,
    and then finds and returns the MVP of the specified year from the appropriate table.

    Parameters:
    year (int): The year for which the MVP is to be fetched.
    league (int, optional): The index of the league's MVP table on the page. Defaults to 0 (NBA).

    Returns:
    str: The name of the MVP if found, otherwise an error message.
    """
        import requests
        import pandas as pd
        from io import StringIO
        url = f"https://www.basketball-reference.com/awards/mvp.html"
        response = requests.get(url)

        tables = pd.read_html(StringIO(response.text))
        
        mvp_table=tables[league]
        if mvp_table is not None:
            index = 2023 - int(year)
            if index in mvp_table.index:
                winner_row = mvp_table.loc[index]

                winner = winner_row.iloc[2]
                return winner
            else:
                return f"Could not find row with year {year} in the table."
        else:
            return "Could not find MVP table on the page."

    def get_nba_championship_winner(year,league=0):
        """
    Fetches the champion of a given year from the basketball-reference playoffs tables.

    This function retrieves the playoffs table from the basketball-reference website
    and identifies the champion team for a specified year. The data is fetched via the 
    `requests` library and parsed using `pandas`.

    Parameters:
    - year (str): The playoff year to search the champion for.
    - league (int): The index of the league's table in the fetched HTML. Default is 0, 
                    typically for the main league's table.

    Returns:
    - str: The name of the champion team of the given year. If the table or specific year
           cannot be found, a corresponding error message is returned.

    Raises:
    - HTTPError: An error occurred during the requests to fetch the data.
    - ValueError: If there is an issue parsing the HTML or locating the data within.

    Example:
     get_nba_championship_winner("2023")
    'Los Angeles Lakers'  # Example output, dependent on actual data and year.
    """
        import requests
        import pandas as pd
        from io import StringIO
        url = f"https://www.basketball-reference.com/playoffs/"
        response = requests.get(url)
        tables = pd.read_html(StringIO(response.text))
        champ_tables=tables[league]
        if champ_tables is not None:
            index = 2024 - int(year)
            if index in champ_tables.index:
                champ_row=champ_tables.loc[index]

                champ = champ_row.iloc[2]
                return champ
            else:
                return f"Could not find row with year {year} in the table."
        else:
            return "Could not find MVP table on the page."

    def get_player_award(player_id, award_name=None):
        """
    Fetches the specific award details for a given player from the NBA API.

    This function uses the NBA API to fetch the awards data for a player specified by their player_id.
    It then filters the awards data to return only the details of the specified award.

    Parameters:
    player_id (int): The ID of the player for whom the award details are to be fetched.
    award_name (str): The name of the award to be fetched.

    Returns:
    DataFrame: A pandas DataFrame containing the details of the specified award for the player.
    """
        from nba_api.stats.endpoints import PlayerAwards
        awards = PlayerAwards(player_id=player_id)
        awards_df = awards.get_data_frames()[0]

    # Filter for the specific award
        if award_name:
            specific_award = awards_df[awards_df['DESCRIPTION'] == award_name]
            return specific_award
        
        return awards_df

    def single_game_records():
        """
    Retrieves the all-time single game scoring leader from the basketball-reference website.

    This function connects to the basketball-reference website's page for single game scoring
    records and extracts the top record using the `requests` and `pandas` libraries. The data 
    is then parsed into a pandas DataFrame to easily access the record holder's information.

    Returns:
    - str: The name of the player with the highest scoring in a single game. If the MVP table 
           cannot be found, a corresponding error message is returned.

    Raises:
    - HTTPError: An error occurred during the requests to fetch the data.
    - ValueError: If there is an issue parsing the HTML or locating the data within.

    Example:
    single_game_records()
    'Wilt Chamberlain'  # Example output, actual data may vary.
    """
        import requests
        import pandas as pd
        from io import StringIO
        url = f"https://www.basketball-reference.com/leaders/pts_game.html"
        response = requests.get(url)

        tables = pd.read_html(StringIO(response.text))
        
        mvp_table=tables[0]
        if mvp_table is not None:
            winner_row = mvp_table.loc[0]
            leader=winner_row.iloc[1]
            return leader
        else:
            return "Could not find MVP table on the page."

    def league_leaders(num=20):
        """
    Fetches the top league leaders from the basketball-reference website.

    This function sends a GET request to the basketball-reference website, parses the HTML response to extract the league leaders table,
    and then returns the top players based on the specified number.

    Parameters:
    num (int, optional): The number of top players to be fetched. Defaults to 20.

    Returns:
    DataFrame: A pandas DataFrame containing the details of the top players if found, otherwise None.
    """
        import pandas as pd
        from bs4 import BeautifulSoup
        import requests
        from io import StringIO
        response = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_leaders.html')
    
        soup = BeautifulSoup(response.content, 'html.parser')
    
        div = soup.find('div', id='leaders_trb_per_g')
    
        if div is not None:
            table = pd.read_html(StringIO(str(div)), flavor='bs4')[0]
            number=int(num)
            if number <=20:
                return table.head(number)
        else:
            return None

    def get_NBA_team_details(team_id)->dict:
        """
    Fetches the details of a specific NBA team using the NBA API.

    This function uses the TeamDetails endpoint from the nba_api.stats module 
    to fetch the details of a specific NBA team. The details are returned as a 
    pandas DataFrame, which is then converted to a dictionary before being returned.

    Args:
        team_id (int): The unique identifier for the NBA team.

    Returns:
        dict: A dictionary containing the details of the NBA team.
    """
        from nba_api.stats.endpoints import TeamDetails
        team=TeamDetails(team_id)
        team_df=team.get_data_frames()[0]
        return team_df

    def get_nba_career_stats(playerid:str):
            """
    Retrieves NBA career statistics for a specified player using the NBA API.

    This function uses the `PlayerCareerStats` endpoint from the `nba_api.stats.endpoints` module
    to fetch career statistics for a player specified by their NBA player ID. The data is returned
    as a pandas DataFrame.

    Parameters:
    - playerid (str): The NBA player's unique identifier.

    Returns:
    - DataFrame: A pandas DataFrame containing the player's career statistics. Each row represents
                 a different season, and each column represents a different statistical category.

    Example:
    get_nba_career_stats('203076')  # Anthony Davis' NBA player ID as an example
    DataFrame output showing stats like games played, points per game, rebounds per game, etc.
    """
            from nba_api.stats.endpoints import PlayerCareerStats
            career_stats = PlayerCareerStats(player_id=playerid)
            career_stats_df = career_stats.get_data_frames()[0]
            return career_stats_df
    
    def get_career_averages(playerid:str,stats='all'):
        """
    Fetches the career averages of a specific NBA player from the NBA API.

    This function uses the NBA API to fetch the career totals of a player specified by their player_id.
    It then calculates the averages for each statistic by dividing the total by the number of games played.
    The function can return either all averages or a specific statistic's average.

    Parameters:
    playerid (str): The ID of the player for whom the career averages are to be fetched.
    stats (str, optional): The specific statistic to be fetched. Defaults to 'all', which returns all averages.

    Returns:
    DataFrame or float: A pandas DataFrame containing all career averages if stats='all', otherwise the average of the specified statistic.
        """
        statColumn={'points':'PTS'}
        from nba_api.stats.endpoints import PlayerCareerStats
        import pandas as pd
        career = PlayerCareerStats(player_id=playerid)
        career_averages = career.career_totals_regular_season
        career_averages_df = career_averages.get_data_frame()

    # Convert columns to numeric values
        for column in career_averages_df.columns:
            if column != 'GP' and column != 'PLAYER_ID':
                career_averages_df[column] = pd.to_numeric(career_averages_df[column], errors='coerce')

    # Calculate averages
        for column in career_averages_df.columns:
            if column != 'GP' and column != 'PLAYER_ID':
                career_averages_df[column] = career_averages_df[column] / career_averages_df['GP']

        if stats != 'all':
            stat = statColumn[stats]
            return career_averages_df.iloc[0][stat]
        else:
            return career_averages_df


    def get_player_game_logs(player_id: str, season=2023,DD=False,TD=False,pts=None,reb=None,ast=None,pf=None,fga=None,fgm=None,tpa=None,tpm=None) -> dict:
        """
        Retrieve a player's game logs for a particular season, with optional filters for double-doubles (DD), triple-doubles (TD), and various statistics.

    Parameters:
    player_id (str): The unique identifier of the player.
    season (int, optional): The season to retrieve game logs for. Defaults to 2023.
    DD (bool, optional): If True, filter for games where the player achieved a double-double. Defaults to False.
    TD (bool, optional): If True, filter for games where the player achieved a triple-double. Defaults to False.
    pts (int, optional): Minimum points for the game log. Defaults to None.
    reb (int, optional): Minimum rebounds for the game log. Defaults to None.
    ast (int, optional): Minimum assists for the game log. Defaults to None.
    pf (int, optional): Minimum personal fouls for the game log. Defaults to None.
    fga (int, optional): Minimum field goal attempts for the game log. Defaults to None.
    fgm (int, optional): Minimum field goals made for the game log. Defaults to None.
    tpa (int, optional): Minimum three-point attempts for the game log. Defaults to None.
    tpm (int, optional): Minimum three-points made for the game log. Defaults to None.

    Returns:
    dict: A dictionary containing the player's game logs that meet the specified criteria.
        """
        from nba_api.stats.endpoints import PlayerGameLog
        game_log=PlayerGameLog(player_id=player_id,season=str(season))
        game_log_df=game_log.get_data_frames()[0]
        if TD:
            pts_value= 10 if pts==None else pts
            reb_value=10 if reb==None else reb
            ast_value=10 if ast==None else ast
            TD_df = game_log_df[(game_log_df['REB'] >= reb_value) & (game_log_df['PTS'] >= pts_value) & (game_log_df['AST'] >= ast_value)]
            return TD_df
        if DD:
            pts_value= 10 if pts==None else pts
            reb_value=10 if reb==None else reb
            ast_value=10 if ast==None else ast
            DD_df = game_log_df[((game_log_df['REB'] >= reb_value) & (game_log_df['PTS'] >= pts_value)) | ((game_log_df['AST'] >= ast_value) & (game_log_df['PTS'] >= pts_value)) | ((game_log_df['AST'] >= ast_value) & (game_log_df['REB'] >= reb_value)) ]
            return DD_df
        
        pts_value=0 if pts==None else pts
        reb_value=0 if reb==None else reb
        ast_value=0 if ast==None else ast
        pf_value=0 if pf==None else pf
        fga_value=0 if fga==None else fga
        fgm_value=0 if fgm==None else fgm
        tpa_value=0 if tpa==None else tpa
        tpm_value=0 if tpm==None else tpm
        game_log_df_searched=game_log_df[(game_log_df['PTS']>=pts_value)& (game_log_df['REB']>=reb_value) & (game_log_df['AST']>=ast_value) & (game_log_df['PF']>=pf_value) & (game_log_df['FGA']>=fga_value) & (game_log_df['FGM']>=fgm_value) & (game_log_df['FG3A']>=tpa_value) & (game_log_df['FG3M']>=tpm_value)]
        return game_log_df_searched
    
    def get_NBA_team_roster(team_id: str,year=2023) -> dict:
        """
   Retrieves the current season roster for a specific NBA team using the NBA API.

    This method queries the NBA API for all players currently active in the league and filters the data
    to return only those players who are on a team specified by the given team ID. The data is managed
    using the `CommonAllPlayers` endpoint and returned as a pandas DataFrame, which is then converted to
    a dictionary.

    Parameters:
    - team_id (str): The unique identifier for the NBA team whose roster is being requested.
    - year (int, optional): The year of the season to fetch the roster for. Defaults to 2023.

    Returns:
    - dict or None: A dictionary representation of the team's roster if the data is successfully fetched.
                    Each key-value pair in the dictionary corresponds to a column and its value for the players
                    on the team. Returns None if there is an error during the fetch operation.

        """
        from nba_api.stats.endpoints import CommonAllPlayers
        try:
            all_players = CommonAllPlayers(league_id="00", season=str(year))
            all_players_df = all_players.get_data_frames()[0]
            team_roster = all_players_df[all_players_df["TEAM_ID"] == team_id]
            return team_roster
        except Exception as e:
            print(f"Error fetching team roster: {e}")
            return None

    def get_team_id(team_info:str) -> dict:
        """
        Retrieves the NBA team ID based on different criteria.

        Args:
        team_info (str): Information about the team (e.g., full name, abbreviation, nickname, city, or state).

        Returns:
        int or None: Team ID if found, or None if not found.
        """
        from nba_api.stats.static import teams
        try:
                team = teams.find_teams_by_full_name(team_info)
                test=team[0]['id']
                if test == None:
                    team = teams.find_team_by_abbreviation(team_info)
                    test=team[0]['id']
                    if test == None:
                        team = teams.find_teams_by_nickname(team_info)
                        test=team[0]['id']
                        if test == None:
                            team = teams.find_teams_by_city(team_info)
                            test=team[0]['id']
                            if test == None:
                                team = teams.find_teams_by_state(team_info)
                                test=team[0]['id']
                                if test==None:
                                    print(f"No team found for '{team_info}'")
                                    return None
                                else:
                                    return test
                            else:
                                return test
                        else:
                            return test
                    else:
                         return test
                else:
                    return test
        except Exception as e:
                print(f"Error fetching team ID: {e}")
                return None

    def AllTimeLeaders() -> dict:
        """
        Retrieve all time leaders in NBA.

        Returns:
        dict: A dictionary containing all time leaders.
        """
        from nba_api.stats.endpoints import AllTimeLeadersGrids
        import pandas as pd
        Leaders = AllTimeLeadersGrids()
    
        if hasattr(Leaders, 'pts_leaders'):
            pts=Leaders.pts_leaders.get_data_frame()
            row=pts.loc[0]
            row_value=row.iloc[1]
        else:
            return "The 'pts_leaders' attribute does not exist in the 'Leaders' object."

        return row_value

    
    def get_team_schedule(Team_id: str,Season='2023',W=False,L=False,FGPT=.000,FG3PT=.000,OREB=0,DREB=0,REB=0,AST=0,STL=0,BLK=0,TOV=50,PF=50,PTS=0) -> dict:
        """
        Filters the team schedule based on specified conditions.

    Args:
        team_id (str): NBA team ID.
        Season (str): Season in the format 'YYYY' (e.g., '2023').
        W (bool): Filter by wins (True) or not (False).
        L (bool): Filter by losses (True) or not (False).
        FGPT (float): Minimum field goal percentage.
        FG3PT (float): Minimum three-point percentage.
        OREB (int): Minimum offensive rebounds.
        DREB (int): Minimum defensive rebounds.
        REB (int): Minimum total rebounds.
        AST (int): Minimum assists.
        STL (int): Minimum steals.
        BLK (int): Minimum blocks.
        TOV (int): Maximum turnovers.
        PF (int): Maximum personal fouls.
        PTS (int): Minimum points scored.

    Returns:
        pd.DataFrame: Filtered team schedule DataFrame.
        """
        from nba_api.stats.endpoints import TeamGameLog
        import pandas as pd
        schedule = TeamGameLog(team_id=Team_id,season=str(Season))
        schedule_data=schedule.get_data_frames()[0]
        schedule_data=schedule_data.drop(['FG3A','FG3M','FGA','FGM','FTA','FTM','Game_ID','L','MIN','Team_ID','W','W_PCT'],axis=1)
        filtered_schedule=schedule_data[(schedule_data['FG_PCT'] >= FGPT)&
        (schedule_data['FG3_PCT'] >= FG3PT) &(schedule_data['OREB'] >= OREB) & (schedule_data['DREB'] >= DREB) & (schedule_data['REB'] >= REB) & (schedule_data['AST'] >= AST) & (schedule_data['STL'] >= STL) &
        (schedule_data['BLK'] >= BLK) & (schedule_data['TOV'] <= TOV) & (schedule_data['PF'] <= PF) & (schedule_data['PTS'] >= PTS)]
        if W:
            Final=filtered_schedule[filtered_schedule['WL']=='W']
            return Final
        elif L:
            Final=filtered_schedule[filtered_schedule['WL']=='L']
            return Final
        else:
            return filtered_schedule
        
    def get_league_standings(season=2023,BR=0) -> dict:
        """
        Retrieve the league standings for a particular season.

        Parameters:
        season (str): The season to retrieve the standings for.
        BR(int,optional): This tells the function if you want to return just the best record for that season

        Returns:
        dict: A dictionary containing the league standings.
        """
        from nba_api.stats.endpoints import LeagueStandings
        import pandas as pd
        standings=LeagueStandings(season=season)
        standings_df=standings.get_data_frames()[0]
        if(BR != 0):
            standings_df['WINS']= pd.to_numeric(standings_df['WINS'], errors='coerce')
            best_team = standings_df['WINS'].idxmax()
            value=standings_df.loc[best_team]  
            name=value['TeamCity']+' '+value['TeamName']
            return name
        return standings_df


    

class MLB:
    def get_player_id(last_name, first_name,bbref=False,retro=False,fangraph=False):
        """
    Retrieves the player's ID based on their last name, first name, and possibly other criteria.

    This function uses the `pybaseball` library to look up the player's ID. It can return the ID from multiple MLB databases
    depending on the flags set.

    Parameters:
    last_name (str): The last name of the player.
    first_name (str): The first name of the player.
    bbref (bool, optional): If True, returns the player's ID from the Baseball-Reference database. Defaults to False.
    retro (bool, optional): If True, returns the player's ID from the Retrosheet database. Defaults to False. (Not implemented in this function)
    fangraph (bool, optional): If True, returns the player's ID from the Fangraphs database. Defaults to False. (Not implemented in this function)

    Returns:
    DataFrame or list: A pandas DataFrame containing the player's ID if bbref is False, otherwise a list containing the player's ID and the last year they played.
    """
        from pybaseball import playerid_lookup
        player_id=playerid_lookup(last_name,first_name)
        if bbref:
            id= player_id['key_bbref']
            id_num=id[0]
            last_played=player_id['mlb_played_last']
            last_year=last_played[0]
            values=[id_num,last_year]
            return values
        return player_id
    
    def get_career_averages(player_info:list):
        """
    Retrieves the career batting average for a specified baseball player from baseball-reference.com.

    This function extracts player data from the specified player's page using their player ID and
    determines the table to parse based on the player's active status. The function returns the player's
    career batting average from the most relevant statistical table. The data extraction is handled using
    `requests` for web scraping and `pandas` for parsing HTML tables.

    Parameters:
    - player_info (list): A list containing the player's ID as a string and their active status as a float.
                          The active status is expected to be the current year (e.g., 2024.0) if they are 
                          currently active.

    Returns:
    - str: The player's career batting average formatted to three decimal places, or an error message if 
           the data cannot be found.

    Example:
    get_career_averages(["johndoe01", 2024.0])
    '0.278'  # Example output, actual data may vary.
    """
        import requests
        import pandas as pd
        player_id=player_info[0]
        player_letter=player_id[0]
        active=player_info[1]
        url = f"https://www.baseball-reference.com/players/{player_letter}/{player_id}.shtml"
        response = requests.get(url)
        tables = pd.read_html(response.text)
        if active==2024.0:
            stats_tables=tables[1]
        else:
            stats_tables=tables[0]
        if stats_tables is not None:
            location=stats_tables.index.size-2
            stat_row=stats_tables.loc[location]
            return "{:.3f}".format(float(stat_row['BA']))
        else:
            return "Could not find MVP table on the page."

    def all_time_leaders(stat_leader):
        """
    Fetches the all-time leader for a specific baseball statistic from the Baseball-Reference website.

    This function sends a GET request to the Baseball-Reference website, parses the HTML response to extract the leaders table,
    and then returns the player who is the all-time leader for the specified statistic.

    Parameters:
    stat_leader (str): The specific statistic for which the all-time leader is to be fetched.

    Returns:
    str: The name of the all-time leader if found, otherwise an error message.
    """
        import requests
        import pandas as pd
        from bs4 import BeautifulSoup
        from io import StringIO
        statColumn={'home runs':'https://www.baseball-reference.com/leaders/HR_career.shtml','hits':'https://www.baseball-reference.com/leaders/H_career.shtml','doubles':'https://www.baseball-reference.com/leaders/2B_career.shtml'}
        link=statColumn[stat_leader]
        url = f"{link}"
        response = requests.get(url)
        tables = pd.read_html(StringIO(response.text))
        stats_tables=tables[0]
        if stats_tables is not None:
            stat_row=stats_tables.loc[0]
            player=stat_row.iloc[1]
            return player
        else:
            return "Could not find Homerun leaders table on the page."

    def get_mvps(year=2023,AL=False,NL=False):
        """
    Retrieves the Major League Baseball (MLB) MVP(s) for a specified year from baseball-reference.com.

    This function fetches the MVP award winner(s) based on the year and the league (American League or National League).
    If both league flags (AL and NL) are False or True, it returns both MVPs for that year; otherwise, it returns
    the MVP for the specified league. The data is extracted from the baseball-reference MVP awards page using `requests`
    and parsed using `pandas`.

    Parameters:
    - year (int, optional): The year to retrieve the MVPs for. Defaults to 2023.
    - AL (bool, optional): Set to True to retrieve the American League MVP. Defaults to False.
    - NL (bool, optional): Set to True to retrieve the National League MVP. Defaults to False.

    Returns:
    - list or str: The name(s) of the MVP(s) as a list if both flags are specified, or a single name if one flag is
                   specified. Returns an error message if the MVP table cannot be found.

    Raises:
    - HTTPError: If there is an issue during the web request.
    - ValueError: If there is an error in calculating the index or parsing the table.

    Example:
    get_mvps(year=2022, AL=True)  # Retrieve the 2022 American League MVP
    'Shohei Ohtani'  # Example output, actual data may vary.
        """
        import requests
        import pandas as pd
        from io import StringIO
        from bs4 import BeautifulSoup
        url = f"{'https://www.baseball-reference.com/awards/mvp.shtml'}"
        response = requests.get(url)
        tables = pd.read_html(StringIO(response.text))
        mvp_table=tables[0]
        if mvp_table is not None:
            index = 2023 - int(year)
            ranges = [(i, i + 2) for i in range(0, mvp_table.index.size+1, 3)]
            if index <= len(ranges):
                if AL != NL :
                    if AL:
                        selected_range=ranges[index][0]
                        stat_row=mvp_table.loc[selected_range]
                        ALplayer=stat_row.iloc[2]
                        return ALplayer
                    if NL:
                         selected_range=ranges[index][0]
                         stat_row=mvp_table.loc[selected_range+1]
                         NLplayer=stat_row.iloc[2]
                         return NLplayer
                else :
                     selected_range=ranges[index]
                     stat_row=mvp_table.loc[selected_range[0]]
                     ALplayer=stat_row.iloc[2]
                     NL_row=mvp_table.loc[selected_range[0]+1]
                     NLplayer=NL_row.iloc[2]
                     MVPS=[ALplayer,NLplayer]
                     return MVPS
        else:
            return "Could not find MVP table on the page."

    def get_best_record(date:int=2024):
        """
        Retrieves the MLB standings for a specific date.

        Parameters:
        date: The specific date for which the standings are requested.

        Returns:
        dict: The MLB standings for the specified date.
        """
        from pybaseball import standings
        import pandas as pd
        teams=[]
        Standings=standings(date)
        length=len(Standings)
        best_team=''
        for x in range(length):
            divison=Standings[x]
            leader=divison.values[0]
            teams.append(leader)
        df=pd.DataFrame(teams)
        value=len(df.index)
        for avg in range(value):
            row=df.loc[avg]
            if best_team == '':
                winPct=float(row[3])
                save=avg
                best_team=row[0]
            elif avg < value-1:
                row2=df.loc[save]
                winPct=float(row[3])
                winPct2=float(row2[3])
                if winPct > winPct2:
                    best_team=row[0]
                    save=avg
                else:
                    best_team=row2[0]
        return best_team

    def get_team_results(team, year,date=None,winner=False,loser=False):
        """
        Retrieves the results of a specific team for a given year.

    This function uses the `schedule_and_record` function from the `pybaseball` module 
    to fetch the results of a specific team for a given year. The results are returned as a 
    pandas DataFrame, which is then converted to a dictionary before being returned.

    Parameters:
    - team (str): The name of the team.
    - year (int): The year for which the results are requested.
    - date (str, optional): The specific date for which the results are requested. Defaults to None.
    - winner (bool, optional): If True, returns only the games where the team won. Defaults to False.
    - loser (bool, optional): If True, returns only the games where the team lost. Defaults to False.

    Returns:
    - dict: A dictionary containing the results of the specified team for the given year. Each key-value 
            pair in the dictionary corresponds to a column and its value for the games on the team's schedule.
            Returns None if there is an error during the fetch operation.

        """
        from pybaseball import schedule_and_record
        results=schedule_and_record(year,team)
        values=[]
        if date:
            for index,row in results.iterrows():
                if row['Date']==date:
                    if winner:
                        if row['Streak']<1:
                            value=get_team_names(row['Opp'])
                            return value
                        else:
                            value=get_team_names(row['Tm'])
                            return value
                        
                    elif loser:
                        if row['Streak']>1:
                            value=get_team_names(row['Tm'])
                            return value
                        else:
                            value=get_team_names(row['Opp'])
                            return value
                    else:
                        return row
        elif winner:
            for index,row in results.iterrows():
                if row['W/L']=='W':
                    values.append(row)
        elif loser:
            for index,row in results.iterrows():
                if row['W/L']=='L':
                    values.append(row)
        return results

    def get_world_series_winner(year=2023,table=0):
        """
    Fetches the winner of the World Series for a specific year from the Baseball-Reference website.

    This function sends a GET request to the Baseball-Reference website, parses the HTML response to extract the World Series table,
    and then returns the team that won the World Series in the specified year.

    Parameters:
    year (int, optional): The year for which the World Series winner is to be fetched. Defaults to 2023.
    table (int, optional): The index of the World Series table on the page. Defaults to 0.

    Returns:
    str: The name of the World Series winner if found, otherwise an error message.
    """
        import requests
        import pandas as pd
        from io import StringIO
        url = f"https://www.baseball-reference.com/postseason/world-series.shtml"
        response = requests.get(url)

        tables = pd.read_html(StringIO(response.text))
        champ_tables=tables[table]
        if champ_tables is not None:
            index = 2023 - int(year)
            if index in champ_tables.index:
                champ_row=champ_tables.loc[index]
                AL_Wins = int(champ_row.iloc[2])
                NL_Wins = int(champ_row.iloc[3])
                if AL_Wins > NL_Wins:
                    return champ_row.iloc[1]
                else:
                    return champ_row.iloc[4]
            else:
                return f"Could not find row with year {year} in the table."
        else:
            return "Could not find world series table on the page."

#---Each of these function that are below this comment is using clingo and gamelogs from 2014-2023
    def get_home_team_wins(requested_season=2023,diff=1,start_date=00000000,end_date=30000000,requested_team=None):
        """
    Fetches the games won by home teams in a specific season from a local Excel file.

    This function reads an Excel file containing game data, processes each game to generate facts about home team wins,
    and then uses the clingo library to solve a logic program based on these facts and some constraints.
    The function returns the games won by home teams where the difference in scores is greater than a specified value.

    Parameters:
    - requested_season (int, optional): The season for which the home team wins are to be fetched. Defaults to 2023.
    - diff (int, optional): The minimum difference in scores for a game to be considered. Defaults to 1.
    - start_date (int, optional): The start date for the period for which the games are to be fetched. Defaults to 00000000.
    - end_date (int, optional): The end date for the period for which the games are to be fetched. Defaults to 30000000.
    - requested_team (str, optional): The team for which the games are to be fetched. If None, games for all teams are fetched. Defaults to None.

    Returns:
    - list: A list of tuples, each containing the game and the home team that won. If there is an error during the fetch operation, an empty list is returned.
    """
        import pandas as pd
        import clingo

        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

        facts = []
        df = pd.read_excel(xls, str(requested_season))
        for i, row in df.iterrows():
                game = row['Date']
                home_team = row['Home Team']
                home_score = row['Home Team Score']
                visiting_score = row['Visting team Score']
                facts.append(f'game("{game}", "{home_team}", {home_score}, {visiting_score}).')

        rules = """
    home_team_won(Game, HomeTeam) :-
    game(Game, HomeTeam, HomeScore, VisitingScore),
    HomeScore > VisitingScore,
    HomeScore - VisitingScore > {0}.

    #show home_team_won/2.
    """.format(diff)

        program = "\n".join(facts) + rules

        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        wins = []
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "home_team_won":
                    game = str(atom.arguments[0])
                    check=game.replace('"','')
                    date= int(check)
                    team = str(atom.arguments[1])
                    teamcheck=team.replace('"','')

                    if date <= end_date and date >start_date:
                        if team:
                            if teamcheck==requested_team:
                                wins.append((game, team))
                        else:
                            wins.append((game, team))
        return wins
    

    def get_extra_inning_walkoffs(requested_team, requested_year=2023):
        """
    Fetches the games won by a specific team in extra innings in a specific season from a local Excel file.

    This function reads an Excel file containing game data, processes each game to generate facts about home team wins,
    and then uses the clingo library to solve a logic program based on these facts and some constraints.
    The function returns the games won by the specified team in extra innings in the specified season.

    Parameters:
    requested_team (str): The team for which the extra inning walkoff wins are to be fetched.
    requested_year (int, optional): The season for which the extra inning walkoff wins are to be fetched. Defaults to 2023.

    Returns:
    list: A list of tuples, each containing the game and the team that won in extra innings.
        """
        import pandas as pd
        import clingo
        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

        facts = []
        df = pd.read_excel(xls, str(requested_year))
        for i, row in df.iterrows():
            game = row['Date']
            home_team = row['Home Team']
            home_score = row['Home Team Score']
            visiting_score = row['Visting team Score']
            length_in_outs = row['Length of Game in Outs']
            season = row['Season']
            facts.append(f'game("{game}", "{home_team}", {home_score}, {visiting_score}, {length_in_outs}, "{season}").')

        rules = """
    extra_inning_walkoff(Game, HomeTeam) :- game(Game, HomeTeam, HomeScore, VisitingScore, LengthInOuts, Season), HomeScore > VisitingScore, LengthInOuts > 54, HomeTeam = "{1}".
    """.format(requested_year, requested_team)

        program = "\n".join(facts) + rules

        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        walkoffs = []
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "extra_inning_walkoff":
                    game = str(atom.arguments[0])
                    walkoffs.append((game))

        return walkoffs

    def get_high_scoring_games( requested_team, requested_score=1,requested_year=None):
        """
    Fetches the high scoring games of a specific team from a local Excel file.

    This function reads an Excel file containing game data, processes each game to generate facts about the scores,
    and then uses the clingo library to solve a logic program based on these facts and some constraints.
    The function returns the games where the specified team scored at least the specified number of runs.

    Parameters:
    requested_team (str): The team for which the high scoring games are to be fetched.
    requested_score (int): The minimum number of runs scored for a game to be considered high scoring.
    requested_year(int): Allows you to only parse through a single table

    Returns:
    list: A list of tuples, each containing the game and the team that scored at least the specified number of runs.
    """
        import pandas as pd
        import clingo
        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

        facts = []
        if requested_year:
            df = pd.read_excel(xls, str(requested_year))
            for i, row in df.iterrows():
                game = row['Date']
                home_team = row['Home Team']
                home_score = row['Home Team Score']
                visiting_team = row['Visting Team']
                visiting_score = row['Visting team Score']
                season = row['Season']
                facts.append(f'game("{game}", "{home_team}", {home_score}, "{visiting_team}", {visiting_score}, "{season}").')
        else:
            for sheet_name in sheet_names:
                df = pd.read_excel(xls, sheet_name)
                for i, row in df.iterrows():
                    game = row['Date']
                    home_team = row['Home Team']
                    home_score = row['Home Team Score']
                    visiting_team = row['Visting Team']
                    visiting_score = row['Visting team Score']
                    season = row['Season']
                    facts.append(f'game("{game}", "{home_team}", {home_score}, "{visiting_team}", {visiting_score}, "{season}").')

        rules = """
    high_scoring_game(Game, Team) :- game(Game, Team, TeamScore, _, _, Season), TeamScore >= {0}, Team = "{1}".
    high_scoring_game(Game, Team) :- game(Game, _, _, Team, TeamScore, Season), TeamScore >= {0}, Team = "{1}".
    """.format(requested_score, requested_team)

        program = "\n".join(facts) + rules

        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        high_scoring_games = []
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "high_scoring_game":
                    game = str(atom.arguments[0])
                    high_scoring_games.append((game))

        return high_scoring_games

    def get_games_with_many_pitchers(requested_team, min_pitchers, requested_year=2023):
        """
    Identifies and returns a list of games where a specified baseball team used a minimum number of pitchers in a given year.

    This function loads game data from an Excel file named 'Data.xlsx', processes the data to extract relevant game information,
    and then uses the `clingo` library for Answer Set Programming (ASP) to identify games that meet the specified criteria of
    pitcher usage. The function processes each sheet in the Excel workbook, constructs ASP facts and rules, and queries these
    facts against the rules to find games where the number of pitchers used by the home team exceeds the specified minimum.

    Parameters:
    - requested_team (str): The name of the team for which the games are queried.
    - min_pitchers (int): The minimum number of pitchers that must have been used in a game for it to be included in the result.
    - requested_year (int, optional): The year for which the games are queried. Defaults to 2023.

    Returns:
    - list of tuples: Each tuple contains the date of the game and the team name, for games that meet the criteria.

    Example:
    get_games_with_many_pitchers("ANA", 5, 2023)
    [("20230326,ANA")]  # Example output
    """
    
        import pandas as pd
        import clingo
        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

  
        facts = []
        df = pd.read_excel(xls, str(requested_year))
        for i, row in df.iterrows():
                game = row['Date']
                home_team = row['Home Team']
                pitchers_used = row['Pitchers Used (H)']
                season = row['Season']
                facts.append(f'game("{game}", "{home_team}", {pitchers_used}, "{season}").')

 
        rules = """
    many_pitchers_game(Game, Team) :- game(Game, Team, PitchersUsed, Season), PitchersUsed > {0}, Season = "{1}", Team = "{2}".
    """.format(min_pitchers, requested_year, requested_team)

        program = "\n".join(facts) + rules

        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        many_pitchers_games = []
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "many_pitchers_game":
                    game = str(atom.arguments[0])
                    many_pitchers_games.append((game))

        return many_pitchers_games

    
    def get_umpire_with_most_runs(requested_season=None):
        """
    Retrieves the umpire who oversaw the most total runs in games for a specified MLB season using data from an Excel file.

    This function processes game data from an Excel workbook named 'Data.xlsx' to calculate the total runs scored in each
    game an umpire oversaw during the specified season. The function uses the `clingo` library to implement Answer Set Programming (ASP)
    that determines which umpire had the highest total run count over the season. The results are aggregated and evaluated 
    using ASP rules and returned in a list.

    Parameters:
    - requested_season (int, optional): The MLB season for which to find the umpire with the most runs observed. Defaults to 2023.

    Returns:
    - list of tuples: Each tuple contains the umpire ID, the season, and the total runs overseen by that umpire.

    Example:
    get_umpire_with_most_runs(2023)
    [('jim123', '2023', 172)]  # Example output, actual data may vary depending on the dataset.
    """
        import pandas as pd
        import clingo
        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

        facts = []
        if requested_season:
            df = pd.read_excel(xls, str(requested_season))
            for i, row in df.iterrows():
                game = row['Date']
                home_score = row['Home Team Score']
                visiting_score = row['Visting team Score']
                season = row['Season']
                umpire = row['Umpire ID(H)']
                if season == requested_season:
                    facts.append(f'game("{game}", {home_score}, {visiting_score}, "{umpire}", "{season}").')
        else:
            for sheet_name in sheet_names:
                df = pd.read_excel(xls, sheet_name)
                for i, row in df.iterrows():
                    game = row['Date']
                    home_score = row['Home Team Score']
                    visiting_score = row['Visting team Score']
                    season = row['Season']
                    umpire = row['Umpire ID(H)']
                    if season == requested_season:
                        facts.append(f'game("{game}", {home_score}, {visiting_score}, "{umpire}", "{season}").')

    # Add the rules
        rules = """
    total_runs(Umpire, Season, Total) :-
    game(_, HomeScore, VisitingScore, Umpire, Season),
    Total = #sum { Run : game(_, HScore, VScore, Umpire, Season), Run = HScore + VScore }.

% Determine which umpire oversaw the most runs in a season
most_runs(Umpire, Season, Max) :-
    total_runs(Umpire, Season, Max),
    #max { Total, U, S : total_runs(U, S, Total), S = Season } = Max,
    Umpire = U.

#show most_runs/3.
    """

        program = "\n".join(facts) + rules
        
        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        most_runs = []
        highestRun=0
        index=0
        counter=0
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "most_runs":
                    umpire = str(atom.arguments[0])
                    season = str(atom.arguments[1])
                    runs = int(str(atom.arguments[2]))
                    if runs>highestRun:
                        highestRun=runs
                        index=counter
                        counter=counter+1
                        most_runs.append((umpire, season, runs))
                    else:
                        counter=counter+1
                        most_runs.append((umpire, season, runs))

        return most_runs[index]

    def get_day_night_wins(requested_season=None,requested_team=None,day=False,night=False):
        """
    Fetches the number of games won by each team during the day and at night from a local Excel file.

    This function reads an Excel file containing game data, processes each game to generate facts about the wins,
    and then uses the clingo library to solve a logic program based on these facts and some constraints.
    The function counts the number of games won by each team during the day and at night.

    Parameters:
    - requested_season (int, optional): The season for which the wins are to be fetched. Defaults to None.
    - requested_team (str, optional): The team for which the wins are to be fetched. If None, wins for all teams are fetched. Defaults to None.
    - day (bool, optional): If True, returns only the games won during the day. Defaults to False.
    - night (bool, optional): If True, returns only the games won at night. Defaults to False.

    Returns:
    - tuple: A tuple of two lists, each containing tuples with the team and the count of wins. The first list contains the day wins and the second list contains the night wins. If there is an error during the fetch operation, an empty tuple is returned.
    """
        import pandas as pd
        import clingo
        xls = pd.ExcelFile('Data.xlsx')

        sheet_names = xls.sheet_names
        sheet_names.remove('teams')

        facts = []
        if requested_season:
            df = pd.read_excel(xls, str(requested_season))
            for i, row in df.iterrows():
                    game = row['Date']
                    home_team = row['Home Team']
                    home_score = row['Home Team Score']
                    visiting_team = row['Visting Team']
                    visiting_score = row['Visting team Score']
                    day_night = row['Day or Night']
                    if home_score > visiting_score:
                        facts.append(f'game("{game}", "{home_team}", "{day_night}").')
                        facts.append(f'win("{game}", "{home_team}").')
                    elif visiting_score > home_score:
                        facts.append(f'game("{game}", "{visiting_team}", "{day_night}").')
                        facts.append(f'win("{game}", "{visiting_team}").')
        else:
            for sheet_name in sheet_names:
                df = pd.read_excel(xls, sheet_name)
                for i, row in df.iterrows():
                    game = row['Date']
                    home_team = row['Home Team']
                    home_score = row['Home Team Score']
                    visiting_team = row['Visting Team']
                    visiting_score = row['Visting team Score']
                    day_night = row['Day or Night']
                    if home_score > visiting_score:
                        facts.append(f'game("{game}", "{home_team}", "{day_night}").')
                        facts.append(f'win("{game}", "{home_team}").')
                    elif visiting_score > home_score:
                        facts.append(f'game("{game}", "{visiting_team}", "{day_night}").')
                        facts.append(f'win("{game}", "{visiting_team}").')

        rules = """
    day_wins(Team, Count) :-
    game(_, Team, "D"),
    Count = #count{ Game : game(Game, Team, "D"), win(Game, Team) }.

night_wins(Team, Count) :-
    game(_, Team, "N"),
    Count = #count{ Game : game(Game, Team, "N"), win(Game, Team) }.

    #show day_wins/2.
    #show night_wins/2.
    """

        program = "\n".join(facts) + rules

        ctl = clingo.Control()

        ctl.add("base", [], program)

        ctl.ground([("base", [])])
        results = ctl.solve(yield_=True)
        day_wins = []
        night_wins = []
        for model in results:
            for atom in model.symbols(shown=True):
                if atom.name == "day_wins":
                    if requested_team:
                        team = str(atom.arguments[0])
                        team=team.replace('"','')
                        if team==requested_team:
                            count = int(str(atom.arguments[1]))
                            day_wins.append((team, count))
                    else:
                        team = str(atom.arguments[0])
                        count = int(str(atom.arguments[1]))
                        day_wins.append((team, count))
                elif atom.name == "night_wins":
                    if requested_team:
                            team = str(atom.arguments[0])
                            team=team.replace('"','')
                            if team==requested_team:
                                count = int(str(atom.arguments[1]))
                                night_wins.append((team, count))
                    else:
                        team = str(atom.arguments[0])
                        count = int(str(atom.arguments[1]))
                        night_wins.append((team, count))

        if day==True:
            return day_wins
        elif night==True:
            return night_wins
        else:
            return day_wins,night_wins
        

    def get_winning_streak(year=2023,requested_team=None):
            """
    Fetches the longest winning streak of each team in a specific season from a local Excel file.

    This function reads an Excel file containing game data, processes each game to generate facts about the wins,
    and then uses the clingo library to solve a logic program based on these facts and some constraints.
    The function calculates the longest winning streak for each team in the specified season.

    Parameters:
    year (str, optional): The season for which the longest winning streaks are to be fetched. Defaults to 2023.
    requested_team(str,optional): Allows the user to get only the longest streak for the team they ask for
    Returns:
    calls a function to check_streaks
    """
            import pandas as pd
            import clingo

            xls = pd.ExcelFile('Data.xlsx')

            sheet_names = xls.sheet_names
            sheet_names.remove('teams')

            facts = []
            team_names={}
            df=pd.read_excel(xls,'teams')
            for i, row in df.iterrows():
                team=row['TEAM']
                city=row['CITY']
                nickname=row['NICKNAME']
                full_name=city+" "+nickname
                team_names[team]=full_name
                facts.append(f'team("{team}").')

            df = pd.read_excel(xls, str(year))
            for i, row in df.iterrows():
                    home_team = row['Home Team']
                    away_team = row['Visting Team']
                    home_score = row['Home Team Score']
                    away_score = row['Visting team Score']
                    if home_score > away_score:
                        game_number=row['Home Team Game Number']
                        season=row['Season']
                        facts.append(f'win("{home_team}", {game_number}, "{season}").')
                    elif away_score > home_score:
                        game_number=row['Visting Team Game Number']
                        season=row['Season']
                        facts.append(f'win("{away_team}", {game_number}, "{season}").')

            rules = """
    streak(T, S, G1, G2) :- 
        win(T, G1, S), win(T, G2, S), G2 - G1 = 1,
        not exists_game_in_between(T, S, G1, G2).

    exists_game_in_between(T, S, G1, G2) :-
        win(T, G, S), G1 = G, G2 = G, G1 < G, G < G2.

    longestStreak(T, S, Max, StartG, EndG) :- 
        team(T),
        win(T, _, S),
        Max = #max{ Length : streak(T, S, G1, G2), Length = G2 - G1 + 1 },
        streak(T, S, StartG, EndG),
        EndG - StartG + 1 = Max.

    #show longestStreak/5.
        """
            program = "\n".join(facts) + rules

            ctl = clingo.Control()

            ctl.add("base", [], program)
            ctl.ground([("base", [])])
            results = ctl.solve(yield_=True)
            streaks = []
            for model in results:
                for atom in model.symbols(shown=True):
                    if atom.name == "longestStreak":
                        team = str(atom.arguments[0])
                        season = str(atom.arguments[1])
                        max_length = int(str(atom.arguments[2]))
                        start_game = int(str(atom.arguments[3]))
                        end_game = int(str(atom.arguments[4]))
                        streaks.append((team, season, max_length, start_game, end_game))

            check_streaks(streaks,team_names,year,requested_team)


def check_streaks(streaks,name,year,requested_team=None):
        """
    Checks the winning streaks of each team in a specific season and prints the longest streak.

    This function sorts the streaks by team, season, and start game, then processes each streak to calculate the length.
    It checks for breaks between streaks and updates the longest streak for each team if necessary.
    Finally, it prints the longest streak for each team in the specified season.

    Parameters:
    streaks (list): A list of tuples, each containing the team, season, length of the streak, and the start and end games of the streak.
    name (dict): A dictionary mapping team abbreviations to full team names.
    year (int): The season for which the longest winning streaks are to be checked.

    Returns:
    None
    """
        streaks.sort(key=lambda s: (s[0], s[1], s[3]))
        prev_streak = None
        longest_streaks = {}
        streakLength=1
        for streak in streaks:
            year_value=int(streak[1].strip('"'))
            if year_value == year:
                if prev_streak:
                    if streak[0] == prev_streak[0] and streak[1] == prev_streak[1]:
                        if streak[3] != prev_streak[4]:
                            streakLength=1
                        elif streak[3] == prev_streak[4]:
                            if streak[2]>streakLength or streakLength>=2:
                                streakLength=streakLength+1
                            if streak[0] not in longest_streaks or streakLength > longest_streaks[streak[0]]:
                                longest_streaks[streak[0]] = streakLength

            prev_streak = streak
        if requested_team:
            for team, streak in longest_streaks.items():
                team = team.strip('"')
                if team==requested_team:
                     print(f"Longest streak for {name[team]} in {year}: {streak} games")
        else:
            for team, streak in longest_streaks.items():
                team = team.strip('"')
                print(f"Longest streak for {name[team]} in {year}: {streak} games")

def date_convertion(date,date_code=False,year_need=False):
    """
    Converts a date string into different formats.

    This function takes a date string and tries to parse it into different formats. It can return the date in the format "mm/dd/yyyy", 
    or as a date code in the format "yyyymmdd". It can also return the day of the week, the month name, and the day of the month as a string, 
    and the year as a separate string.

    Parameters:
    - date (str): The date string to be converted.
    - date_code (bool, optional): If True, returns the date as a date code. Defaults to False.
    - year_need (bool, optional): If True, returns the year as a separate string. Defaults to False.

    Returns:
    - str or tuple: Depending on the parameters, the function can return a string or a tuple of strings. If there is an error during the conversion, an empty string or tuple is returned.
    """
    from datetime import datetime
    values=[]
    try:
        date=date.replace('"', '')
        parsed_date = datetime.strptime(date, '%Y%m%d')
        formatted_date = parsed_date.strftime("%m/%d/%Y")
        return formatted_date
    except:
        pass
    try:
        check=datetime.strptime(date,'%B %d %Y')
        date_obj = check
        if date_code:
            formatted_date = date_obj.strftime('%Y%m%d')
            return formatted_date
        day_of_week = date_obj.strftime('%A')
        month_name = date_obj.strftime('%b')
        day_of_month = int(date_obj.strftime('%d'))
        full_word= day_of_week+', '+ month_name+' '+str(day_of_month)
        values.append(full_word)
        year=date_obj.strftime('%Y')
        values.append(year)
    except:
        date_obj = datetime.strptime(date, '%m/%d/%Y')
        if date_code:
            formatted_date = date_obj.strftime('%Y%m%d')
            if year_need:
                year=date_obj.strftime('%Y')
                return formatted_date,year
            else:
                return formatted_date
        day_of_week = date_obj.strftime('%A')
        month_name = date_obj.strftime('%b')
        day_of_month = int(date_obj.strftime('%d'))
        full_word= day_of_week+', '+ month_name+' '+str(day_of_month)
        values.append(full_word)
        year=date_obj.strftime('%Y')
        values.append(year)
    return values

def get_team_names(abbrivation=None,nickname=None,RetroName=None,retro=False):
        """
    Fetches the team names based on the abbreviation, nickname, or retro name.

    This function reads two Excel files containing team data. It can return the team name based on the abbreviation or nickname.
    It can also return the team name based on the retro name if the 'retro' parameter is set to True.

    Parameters:
    - abbrivation (str, optional): The abbreviation of the team. Defaults to None.
    - nickname (str, optional): The nickname of the team. Defaults to None.
    - RetroName (str, optional): The retro name of the team. Defaults to None.
    - retro (bool, optional): If True, the function returns the team name based on the retro name. Defaults to False.

    Returns:
    - str: The name of the team. If there is an error during the fetch operation, an empty string is returned.
        """
        import pandas as pd
        if retro:
            xls = pd.ExcelFile('Data.xlsx')
            df = pd.read_excel(xls, 'teams')
            for i, row in df.iterrows():
                team=row['TEAM']
                city=row['CITY'].lower()
                Nickname=row['NICKNAME'].lower()
                if RetroName==Nickname:
                    return team
                else:
                    full_Name=city+" "+Nickname
                    if full_Name==RetroName:
                        return team
                    
        xls = pd.ExcelFile('MLB Team Abbrivation.xlsx')
        df=pd.read_excel(xls,'Names')
        for i, row in df.iterrows():
            if abbrivation is not None:
                abb=row['Abbreviation']
                name=row['Team Name']
                if abb==abbrivation:
                    return name
            if nickname is not None:
                abb=row['Abbreviation']
                nname=row['Nickname'].lower()
                if nname==nickname:
                    return abb

def get_umpire_name(ID,year):
     """
    Fetches the name of an umpire based on their ID and the year.

    This function reads an Excel file containing umpire data for a specific year. It iterates over each row in the DataFrame 
    to find the umpire with the matching ID. If the umpire is found, it returns their full name (first name and last name). 
    If the umpire is not found, it prints a message indicating that the umpire's name could not be found.

    Parameters:
    - ID (str): The ID of the umpire.
    - year (int): The year for which the umpire data is to be fetched.

    Returns:
    - str: The name of the umpire. If the umpire is not found, an empty string is returned.
    """
     import pandas as pd
     xls = pd.ExcelFile('UMPIRE.xlsx')
     df = pd.read_excel(xls, str(year))
     for i, row in df.iterrows():
         ID_Ump=row['ID']
         if ID_Ump==ID:
             first_name=row['first']
             last_name=row['last']
             name=first_name+" "+last_name
             return name
     print('Unable to find the umpires name')

