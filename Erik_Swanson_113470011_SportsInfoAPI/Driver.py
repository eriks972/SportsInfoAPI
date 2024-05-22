from SportsInfoAPI import NBA
from SportsInfoAPI import MLB
import SportsInfoAPI
import pandas as pd
class UserInterface:
    def __init__(self, api):
        self.api = api

    def start(self):
        print('Welcome to SportsInfo')
        while True:
            print('Please Select one of the option below: ')
            print("\n1. Get player info")
            print("2. Get team info")
            print("3. Use our sports query systems")
            print("4. Ask questions ")
            print('5. View Standings')
            print('6. Records and Leaders')
            print('7. Quit')
            choice = input("Please choose an option: ")

            if choice == '1':
                self.get_player_info()

            elif choice == '2':
                self.get_team_info()

            elif choice == '3':
                query_system = input('Would you like to use our NBA or MLB query system? (NBA/MLB): ')
                if query_system.lower() == 'nba':
                    exec(open("NBA_Query.py").read())
                elif query_system.lower() == 'mlb':
                    exec(open("MLB_query.py").read())

            elif choice=='4':
                sport = input("Enter the sport (MLB or NBA): ")
                if sport.lower() == 'nba':
                    print("1: Who won the MVP in a certain season")
                    print("2: Who won the finals in a certain season")
                    choice=("Which question do you want? ")
                    if choice=='1':
                        year=input("What year do you want?")
                        answer=NBA.get_mvp(year)
                        print(answer)
                    elif choice=='2':
                        year=input("What year do you want?")
                        answer=NBA.get_nba_championship_winner(year)
                        print(answer)
                elif sport.lower() == 'mlb':
                    print("1: Who won the MVP in a certain season")
                    print("2: Who won the world series in a certain season")
                    print("3. Who had the best record in a particular season?")
                    print('4. Which umpire allowed the most runs in a particular season?')
                    choice=("Which question do you want? ")
                    if choice=='1':
                        year=input("What year do you want?")
                        choice=input('Do you want the American league,National league or both?')
                        if choice.lower()=='american' or 'american league':
                            info=MLB.get_mvps(year,True)
                            print(f'The American league MVP in {year} was {info}')
                        elif choice.lower()=='national' or 'national league':
                            mvp=MLB.get_mvps(year,False,True)
                            print(f'The National league MVP in {year} was {mvp}')
                        else:
                            mvp=MLB.get_mvps(year)
                            print(f'The MVPs in {year} were {mvp[0]} and {mvp[1]} ')
                    if choice=='2':
                        year=input("What year do you want?")
                        info=MLB.get_world_series_winner(int(year))
                        print(info)
                    if choice=='3':
                        year=int(input("What year do you want?"))
                        info=MLB.get_best_record(year)
                    if choice=='4':
                        year=input("What year do you want?")
                        test=MLB.get_umpire_with_most_runs(int(year))
                        umpire_ID=test[0].replace('"','')
                        name=SportsInfoAPI.get_umpire_name(umpire_ID,test[1].replace('"',''))
                        print(f'The umpire who was behind the plate with the most runs scored in {year} was {name} with {test[2]} runs scored')
            elif choice=='5':
                sport = input("Enter the sport (MLB or NBA): ")
                if sport.lower() == 'NBA':
                    year=input('Please enter the year you would like')
                    choice=input('Would you like to know who had the best record(Y/N)?')
                    if choice.lower()=='y':
                        info=NBA.get_league_standings(year,1)
                        print(info)
                    else:
                        info=NBA.get_league_standings(year)
                        print(info)
            elif choice=='6':
                sport = input("Enter the sport (MLB or NBA): ")
                if sport.lower() == 'nba':
                    print('1: Single Game Record')
                    print('2: All Time Leaders')
                    print('3: League Leaders')
                    choice=input('Which one do you want? ')
                    if choice=='1':
                        info=NBA.single_game_records()
                        print(info)
                    if choice=='2':
                        info=NBA.AllTimeLeaders()
                        print(info)
                    if choice=='3':
                        number=int(input('How many players do you want to see: '))
                        info=NBA.league_leaders(number)
                        print(info)
                if sport.lower()=='mlb':
                    print('1: All Time Leaders')
                    choice=input('Which one do you want? ')
                    if choice=='1':
                        info=MLB.all_time_leaders('home runs')
                        print(info)
            elif(choice=='7'):
                break
            else:
                print("Invalid option. Please try again.")
            another_query = input("Do you want to do another query? (yes/no): ")
            if another_query.lower() != 'yes':
                break
       
    def get_player_info(self):
        sport = input("Enter the sport (MLB or NBA): ")
        if sport.lower() == 'nba':
            player = self.get_NBA_Player()
        elif sport.lower() == 'mlb':
            player = self.get_MLB_Player()
        while True:
            print("1. Career Stats")
            print("2. Career Averages")
            print("3. Game Logs")
            print("4. Awards")
            print("5. Quit")
            choice = input("Please choose an option: ")

            if choice == '1':
               if sport.lower()=='nba':
                   info=NBA.get_nba_career_stats(player)
                   print(info)
               elif sport.lower()=='mlb':
                    print('We do not hav any systems for MLB for this choice')
            elif choice == '2':
                if sport.lower()=='nba':
                    info=NBA.get_career_averages(player)
                    print(info)
                if sport.lower()=='mlb':
                    info=MLB.get_career_averages(player)
                    print(info)
            elif choice == '3':
                if sport.lower()=='nba':
                    year=input("Enter the season you would like to see: ")
                    choice=input("Do you want to filter out any games from this players game logs?(Y/N) ")
                    TD=False
                    DD=False
                    points=None
                    rebounds=None
                    assists=None
                    fouls=None
                    fga=None
                    fgm=None
                    tfga=None
                    tfgm=None
                    if choice.lower()=='y':
                        print('1: Points')
                        print('2: Rebounds')
                        print('3: Assists')
                        print('4: Fouls')
                        print('5: Field Goals Attempted')
                        print('6: Field Goals Made')
                        print('7: Threes Attempted')
                        print('8: Threes Made')
                        print('9: Triple Doubles')
                        print('10: Double Doubles')
                        while True:  
                            choice=input('Which stat do you want to filter by(enter the number): ')
                            if choice=='1':
                                points=int(input('How Many Points: '))
                            elif choice=='2':
                                rebounds=int(input('How Many Rebounds: '))
                            elif choice=='3':
                                assists=int(input('How Many Assists: '))
                            elif choice=='4':
                                fouls=int(input('How Many Fouls: '))
                            elif choice=='5':
                                fga=int(input('How Many field goals attempted: '))
                            elif choice=='6':
                                fgm=int(input('How Many field goals made: '))
                            elif choice=='7':
                                tfga=int(input('How Many threes attempted: '))
                            elif choice=='8':
                                tfgm=int(input('How Many threes made: '))
                            elif choice=='9':
                                TD=bool(True)
                            elif choice=='10':
                                DD=bool(True)
                            else:
                                print('Try again')
                            another_filter = input("Do you want to add another filter? (Y/N): ")
                            if another_filter.lower() != 'y':
                                break
                      
                    info=NBA.get_player_game_logs(player,year,DD,TD,points,rebounds,assists,fouls,fga,fgm,tfga,tfgm)
                    print(info)
                elif sport.lower()=='mlb':
                    print('We do not hav any systems for MLB for this choice')
            elif choice=='4':
                if sport.lower() == 'nba':
                    award=input('Would you like to see all the awards the player has won?(Y/N)')
                    if award.lower()=='y':
                        info=NBA.get_player_award(player)
                        print(info)
                    else:
                        while True:
                            award=input('Which award do you want to see?(i for list)')
                            if award.lower()=='i':
                                print('NBA Finals Most Valuable Player')
                                print('NBA All-Star Most Valuable Player')
                                print('NBA Sporting News Most Valuable Player of the Year')
                                print('NBA In-Season Most Valuable Player')
                                print('NBA Most Valuable Player')
                                print('NBA Rookie of the Month')
                                print('NBA Player of the Week')
                                print('NBA Rookie of the Year')
                                print('NBA Player of the Month')
                                print('Olympic Bronze Medal')
                                print('Olympic Silver Medal')
                                print('Olympic Gold Medal')
                                print('NBA In-Season Tournament All-Tournament')
                                print('All-NBA')
                                print('All-Defensive Team')
                                print('All-Rookie Team')
                            elif award.lower()!='i':
                                info=NBA.get_player_award(player,award)
                                print(info)
                elif sport.lower()=='mlb':
                    print('We do not hav any systems for MLB for this choice')
            elif choice=='5':
                break
            else:
                print("Invalid option. Please try again.")

    def get_NBA_Player(self):
        while True:
            print("\n1. Look up by ID")
            print("2. Look up by Name")
            print("3. Look up by team roster")
            print("4. Quit")
            choice = input("How do you want to look up the player: ")
            if choice == '1':
                ID=input("Enter Player ID: ")
                return ID
            elif choice == '2':
                Last=input("Enter the Players last Name: ")
                First=input("Enter the Players First Name: ")
                return NBA.get_player_ID_NBA(Last,First)
            elif choice == '3':
                word=input("Enter your entry: ")
                team_id=NBA.get_team_id(word)
                info=NBA.get_NBA_team_roster(team_id)
                player_info = info[["PERSON_ID", "DISPLAY_FIRST_LAST"]]
                player_tuples = [(row["PERSON_ID"], row["DISPLAY_FIRST_LAST"]) for _, row in player_info.iterrows()]
                for i, (_, player_name) in enumerate(player_tuples, start=1):
                    print(f"{i}. {player_name}")
                number=int(input("Enter the number player you desire: "))
                if 1 <= number <= len(player_tuples):
                    return player_tuples[number - 1][0]

    def get_MLB_Player(self):
       while True:
           last=input('Please Enter the players last name: ')
           first=input('Please Enter the players first name: ')
           return MLB.get_player_id(last,first,True)

    def get_team_info(self):
        sport = input("Enter the sport (MLB or NBA): ")
        if(sport.lower()=='nba'):    
            word=input("Enter your entry: ")
            team_id=NBA.get_team_id(word)
        while True:
            print("1. Rosters")
            print("2. Team Schedule")
            print('3. Team Details')
            print('4. Questions')
            print("5. Quit")
            choice = input("Please choose an option: ")
            if choice=='1':
                if sport.lower()=='nba':
                    year=input('What year do you want: ')
                    info=NBA.get_NBA_team_roster(team_id,year)
                    print(info)
                elif sport.lower()=='mlb':
                    print('We do not hav any systems for MLB for this choice')
            elif choice == '2':
                if sport.lower()=='nba':
                    Season=input('What season do you want: ')
                    choice=input('Would you like to filter out games from the schedule(Y/N)? ')
                    wins=False
                    losses=False
                    points=None
                    rebounds=None
                    assists=None
                    fouls=None
                    fgpt=None
                    dreb=None
                    oreb=None
                    tfpt=None
                    stl=None
                    blk=None
                    TO=None
                    if choice.lower=='Y':
                        print('1: Field Goal Percentage')
                        print('2: Three Point Percentage')
                        print('3: Offensive Rebounds')
                        print('4: Defensive Rebounds')
                        print('5: Rebounds')
                        print('6: Assists')
                        print('7: Steals')
                        print('8: Blocks')
                        print('9: Turnovers')
                        print('10: Fouls')
                        print('11. Points')
                        print('12. Wins')
                        print('13. losses')
                        while True:  
                            choice=input('Which stat do you want to filter by(enter the number): ')
                            if choice=='11':
                                points=int(input('How Many Points: '))
                            elif choice=='5':
                                rebounds=int(input('How Many Rebounds: '))
                            elif choice=='6':
                                assists=int(input('How Many Assists: '))
                            elif choice=='10':
                                fouls=int(input('How Many Fouls: '))
                            elif choice=='3':
                                oreb=int(input('Offensive Rebounds: '))
                            elif choice=='4':
                                dreb=int(input('Defensive Rebounds: '))
                            elif choice=='2':
                                tfpt=int(input('Threes Percenatge:  '))
                            elif choice=='1':
                                fgpt=int(input('Field Goal Percentge: '))
                            elif choice=='8':
                                blk=int(input('Blocks: '))
                            elif choice=='7':
                                stl=int(input('Steals:  '))
                            elif choice=='9':
                                to=int(input('Turnovers: '))
                            elif choice=='12':
                                wins=bool(True)
                            elif choice=='13':
                                losses=bool(True)
                            else:
                                print('Try again')
                            another_filter = input("Do you want to add another filter? (Y/N): ")
                            if another_filter.lower() != 'y':
                                break
                    info=NBA.get_team_schedule(team_id,Season,wins,losses,fgpt,tfpt,oreb,dreb,rebounds,assists,stl,blk,to,fouls,points)
                    with pd.option_context('display.max_rows', None):
                            print(info)
                if sport.lower()=='mlb':
                    date=None
                    winner=None
                    loser=None
                    choice=input('Please enter the name without the city name(ex. yankees)? ')
                    team=SportsInfoAPI.get_team_names(nickname=choice)
                    date=input('Enter the date(ex: 04/12/2023): ')
                    date=SportsInfoAPI.date_convertion(date)
                    question2=input('Do you want specficially the winner or the loser(Y/N)? ')
                    if question2.lower()=='y':
                        choices=input('winner or loser? ')
                        if choices.lower()=='winner':
                            winner=True
                        elif choices.lower()=='loser': 
                            loser=True
                    info=MLB.get_team_results(team,int(date[1]),date[2],winner,loser)
                    print(info)
            elif choice=='3':
                if sport.lower()=='nba':
                    info=NBA.get_NBA_team_details(team_id)
                    print(info)
                elif sport.lower()=='mlb':
                    print('We do not hav any systems for MLB for this choice')
            elif choice=='4':
                if sport.lower()=='nba':
                    print('We do not hav any systems for NBA for this choice')
                elif sport.lower()=='mlb':
                    print('1. Home Team wins that happened for between two dates for a particular team')
                    print('2. Extra Inning walkoffs in a particular season by a specfic team')
                    print('3. Games where a specfic team scored a certain amount of runs')
                    print('4. Games where a certain amount of pitchers were used by a team in a season')
                    print('5. Wins in the day or night by a specfic team ')
                    print('6. Longest winning streak in a season by a team')
                    while True:
                        choice=input('Which question do you want to answer? ')
                        if choice=='1':
                            year=input('What year do you want: ')
                            diff=input('Enter a score difference if you want(1 is default): ')
                            if diff=='':
                                diff=None
                            startdate=input('Enter a start date to look for if you want(MM/DD/YYYY)?: ')
                            if startdate!='':
                                startdate=SportsInfoAPI.date_convertion(startdate,True)
                            enddate=input('Enter a end date to look for if you want(MM/DD/YYYY)?: ')
                            if enddate!='':
                                enddate=SportsInfoAPI.date_convertion(enddate,True)
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)   
                            info=MLB.get_home_team_wins(year,diff,startdate,enddate,team)
                            print(f'The {team} won {len(info)} games')
                            for games in info:
                                games=games[0].replace('"','')
                                print(SportsInfoAPI.date_convertion(games))
                        elif choice=='2':
                            year=input('What year do you want: ')
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)   
                            info=MLB.get_extra_inning_walkoffs(team,year)
                            print(f"This Team had {len(info)} extra inning walkoffs in {year}")
                            for wins in info:
                                print(SportsInfoAPI.date_convertion(wins))
                        elif choice=='3':
                            year=input('What year do you want: ')
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)
                            score=int(input('Enter a Score you want the team to have scored(1 is default): '))   
                            info=MLB.get_high_scoring_games(team,score,year)
                            print(f"This Team had {len(info)} games where they scored at least {score} in {year}")
                            for wins in info:
                                print(SportsInfoAPI.date_convertion(wins))
                        elif choice=='4':
                            year=input('What year do you want: ')
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)
                            pitchers_used=int(input('How many Pitchers do you want the team to use'))
                            info=MLB.get_games_with_many_pitchers(team,pitchers_used,year)
                            print(f"This Team had {len(info)} games with at least {pitchers_used} pitchers used at in {year}")
                            for wins in info:
                                print(SportsInfoAPI.date_convertion(wins))
                        elif choice=='5':
                            day=False
                            night=False
                            year=input('What year do you want: ')
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)
                            time_of_day=input("Do you want day, night or both? ")
                            if time_of_day.lower()=='day':
                                day=True
                            elif time_of_day.lower()=='night':
                                night=True
                            info=MLB.get_day_night_wins(year,team,day,night)
                            if day:
                                print(f'The {team} had {info[0][1]} wins in day games in {year}')
                            elif night:
                                print(f'The {team} had {info[0][1]} wins in night games in {year}')
                            else:
                                print(f'The {team} had {info[0][1]} wins in day games and {info[1][1]} in night games in {year}')
                        elif choice=='6':
                            year=input('What year do you want: ')
                            choice=input('Please enter the name without the city name(ex. yankees)? ')
                            team=SportsInfoAPI.get_team_names(RetroName=choice,retro=True)
                            info=MLB.get_winning_streak(year,team)
                        else:
                            print('Please enter a different choice!')
            elif choice=='5':
                break
            else:
                print("Invalid option. Please try again.")

def main():
    api = NBA
    ui = UserInterface(api)
    ui.start()

if __name__ == "__main__":
    main()