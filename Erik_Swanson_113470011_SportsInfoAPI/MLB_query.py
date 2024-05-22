import nltk
from nltk.tokenize import word_tokenize
from SportsInfoAPI import MLB
import SportsInfoAPI
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.corpus import stopwords
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_trf')

# Process user input
user_query = input("Ask me an MLB-related question: ").lower()

user_query=user_query.replace("-"," ")

tokens = nltk.word_tokenize(user_query)

bigram_finder = BigramCollocationFinder.from_words(tokens)

# Find the top 10 bigrams
top_10_bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

# Create bigram collocation finder
Trigram_finder = TrigramCollocationFinder.from_words(tokens)

# Find the top 10 bigrams
top_10_trigrams = Trigram_finder.nbest(TrigramAssocMeasures.likelihood_ratio, 10)

known_Bi_combinations=[("career","stats"),("career","average"),('play','for'),('best', 'record'),('all','time'),('world','series'),('batting','average'),('home','run'),('american','league'),('national','league'),('extra','innings'),('extra','inning'),('at','least'),('most','runs'),('day','record'),('night','record'),('home','wins'),('home','win')]

known_Tri_combinations=[('all','time','leading'),('all','time','leader'),('longest','winning','streak'),('day','night','splits'),('record','in','day'),('record','in','night'),('win','at','home')]

stats=['average']

words=["team",'championship','champions','World Series','al','nl','won','lost','walkoff','walkoffs','scored','pitchers','umpire','day','night','home']

award=['mvp']

matching_bigrams = [bigram for bigram in top_10_bigrams if bigram in known_Bi_combinations]

matching_trigrams = [trigram for trigram in top_10_trigrams if trigram in known_Tri_combinations]

matching_stats = [stat for stat in stats if stat in tokens]

matching_words=[word for word in words if word in tokens]

awards=[trophy for trophy in award if trophy in tokens]

# Use spaCy for Named Entity Recognition
doc = nlp(user_query)

# Identify player names in the user's query
players = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
teams = [ent.text for ent in doc.ents if ent.label_ == 'ORG' and ent.text != 'mlb']
year = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
numbers = [ent.text for ent in doc.ents if ent.label_ == 'CARDINAL']


# If a player name is found, fetch the player's stats
if players:
    for player in players:
        first_name, last_name = player.split()
        player_id = MLB.get_player_id(last_name,first_name,True)
        if player_id:
            if matching_bigrams ==[('career', 'stats')] :
                pass
            elif matching_bigrams == [('career','average')] or [('batting','average')]:
                        player_stats=MLB.get_career_averages(player_id)
                        print(f'The Career Batting Average for {first_name} {last_name} is {player_stats}')  
            elif matching_bigrams==[('play','for')]:
                pass
        else:
            print(f"I'm sorry, I couldn't find stats for {player}.")

elif teams:
    stop_words = set(stopwords.words('english'))
    teams_without_stopwords = [' '.join(word for word in word_tokenize(team) if word not in stop_words) for team in teams]
    for team in teams_without_stopwords:
        if matching_words:
             for words in matching_words:
                  if words=='won':
                       if year:
                            for dates in year:
                                 teamabb=SportsInfoAPI.get_team_names(nickname=team)
                                 date=SportsInfoAPI.date_convertion(dates)
                                 print(MLB.get_team_results(teamabb,int(date[1]),date[0],True))
                  if words=='lost':
                        if year:
                            for dates in year:
                                 teamabb=SportsInfoAPI.get_team_names(nickname=team)
                                 date=SportsInfoAPI.date_convertion(dates)
                                 print(MLB.get_team_results(teamabb,int(date[1]),date[0],loser=True))
                  if words=='home':
                       if matching_trigrams:
                            for trigrams in matching_trigrams:
                                 if trigrams==('win','at','home'):
                                      if year:
                                        for dates in year:
                                            teamName=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                            date=SportsInfoAPI.date_convertion(dates,True,True)
                                            test=MLB.get_home_team_wins(int(date[1]),end_date=int(date[0]),requested_team=teamName)
                                            print(f'The {team} won {len(test)} games before {dates}')
                                            for games in test:
                                                 games=games[0].replace('"','')
                                                 print(SportsInfoAPI.date_convertion(games))

                  if words=='walkoff' or 'walkoffs':
                       if matching_bigrams:
                            for bigrams in matching_bigrams:
                                 if bigrams==[('extra','innings')] or [('extra','inning')]:
                                    if year:
                                        for dates in year:
                                            teamName=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                            walkoffs=MLB.get_extra_inning_walkoffs(teamName,dates)
                                            print(f"This Team had {len(walkoffs)} extra inning walkoffs in {dates}")
                                            for wins in walkoffs:
                                                print(SportsInfoAPI.date_convertion(wins))
                  if words=='scored':
                        if numbers:
                            for num in numbers:
                                if year:
                                    for dates in year:
                                        teamName=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                        game_scored=MLB.get_high_scoring_games(teamName,int(num),dates)
                                        print(f"This Team had {len(game_scored)} games where they scored at least {num} in {dates}")
                                        for wins in game_scored:
                                            print(SportsInfoAPI.date_convertion(wins))
                  if words=='pitchers':
                        if numbers:
                            for num in numbers:
                                if year:
                                    for dates in year:
                                         teamName=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                         pitchers_used=MLB.get_games_with_many_pitchers(teamName,4,dates)
                                         print(f"This Team had {len(pitchers_used)} games with at least {num} pitchers used at in {dates}")
                                         for wins in pitchers_used:
                                            print(SportsInfoAPI.date_convertion(wins))
                  if words=='day' or 'night':
                       if year:
                            for dates in year:
                                if matching_bigrams==[('day','record')] or matching_trigrams==[('record','in','day')]:
                                    team=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                    test=MLB.get_day_night_wins(int(dates),team,day=True)
                                    print(f'The {team} had {test[0][1]} wins in day games in {dates}')
                                elif matching_bigrams==[('night','record')] or matching_trigrams==[('record','in','night')]:
                                    team=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                    test=MLB.get_day_night_wins(int(dates),team,night=True)
                                    print(f'The {team} had {test[0][1]} wins in night games in {dates}')
                                elif matching_trigrams==[('day','night','splits')]:
                                    team=SportsInfoAPI.get_team_names(RetroName='yankees',retro=True)
                                    test=MLB.get_day_night_wins(int(dates),team)
                                    print(f'The {team} had {test[0][1]} wins in day games and {test[1][1]} in night games in {dates}')
        if matching_trigrams:
             for trigrams in matching_trigrams:
                  if trigrams == ('longest', 'winning', 'streak'):
                        if year:
                            for dates in year:
                                teamname=SportsInfoAPI.get_team_names(RetroName=team,retro=True)
                                MLB.get_winning_streak(int(dates),requested_team=teamname)
                       
elif awards:
    for trophy in awards:
        if trophy == 'mvp':
            if year:
                for years in year:
                    if matching_bigrams or matching_words:
                        if matching_bigrams==[('american','league')] or words=='al':
                            mvp=MLB.get_mvps(years,True)
                            print(f'The American league MVP in {years} was {mvp}')
                        elif matching_bigrams==[('national','league')] or words=='nl':
                            mvp=MLB.get_mvps(years,False,True)
                            print(f'The National league MVP in {years} was {mvp}')
                    else:
                        mvp=MLB.get_mvps(years)
                        print(f'The MVPs in {years} were {mvp[0]} and {mvp[1]} ')
elif matching_words:
     for words in matching_words:
          if words=='umpire':
               if matching_bigrams:
                    for bigrams in matching_bigrams:
                         if bigrams==('most','runs'):
                              if year:
                                for years in year:
                                     test=MLB.get_umpire_with_most_runs(int(years))
                                     umpire_ID=test[0].replace('"','')
                                     name=SportsInfoAPI.get_umpire_name(umpire_ID,test[1].replace('"',''))
                                     print(f'The umpire who was behind the plate with the most runs scored in {years} was {name} with {test[2]} runs scored')
elif year:
     if matching_bigrams==[('best', 'record')]:
            for years in year:
               best_record=MLB.get_best_record(int(years))
               print(f"The team with the best record in {years} is {best_record}")
     if matching_bigrams == [('world','series')]:
            for years in year:
                Championship=MLB.get_world_series_winner(int(years))
                print(Championship)
elif numbers:
    pass
elif matching_bigrams:
        if matching_bigrams == [('all','time')]:
           all_time=MLB.all_time_leaders('home runs')
           print(all_time)
           pass                  
else:
    print("I'm sorry, I don't understand that MLB query.")
