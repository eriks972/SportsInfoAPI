import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from SportsInfoAPI import NBA
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.corpus import stopwords
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_trf')

# Process user input
user_query = input("Ask me an NBA-related question: ").lower()

user_query=user_query.replace("-"," ")

tokens = nltk.word_tokenize(user_query)

bigram_finder = BigramCollocationFinder.from_words(tokens)

# Find the top 10 bigrams
top_10_bigrams = bigram_finder.nbest(BigramAssocMeasures.likelihood_ratio, 10)

# Create bigram collocation finder
Trigram_finder = TrigramCollocationFinder.from_words(tokens)

# Find the top 10 bigrams
top_10_trigrams = Trigram_finder.nbest(TrigramAssocMeasures.likelihood_ratio, 10)

known_Bi_combinations=[("career","stats"),("career","average"),('play','for'),('best', 'record'),('all','time'),('most','points'),('all','star'),('sporting','news'),('in','season'),('rookie','month'),('rookie','year'),('player','month'),('player','week'),('bronze','medal'),('silver','medal'),('gold','medal'),('all','tornament'),('all','defense'),('all','nba'),('all','rookie'),('double','doubles'),('triple','doubles'),('threes','made'),('threes','attempted'),('played','for'),('plays','for'),('offensive','rebounds'),('defense','rebounds')]

known_Tri_combinations=[('career', 'average', 'points'),('current', 'nba', 'season'),('all','time','leading'),('all','time','leader'),('field','goals','made'),('field','goals','attempted')]

stats=["points","rebounds","assists"]

words=["team",'championship','champions','finals','roster','wins','losses','fouls','turnovers']

award=['mvp','rookie','player','medal']

staters=['rebounders','scorers','assistors']

matching_bigrams = [bigram for bigram in top_10_bigrams if bigram in known_Bi_combinations]

matching_trigrams = [trigram for trigram in top_10_trigrams if trigram in known_Tri_combinations]

matching_stats = [stat for stat in stats if stat in tokens]

matching_words=[word for word in words if word in tokens]

awards=[trophy for trophy in award if trophy in tokens]

stat_people= [people for people in staters if people in tokens]

# Use spaCy for Named Entity Recognition
doc = nlp(user_query)

# Identify player names in the user's query
players = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
teams = [ent.text for ent in doc.ents if ent.label_ == 'ORG' and ent.text != 'nba']
year = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
numbers = [ent.text for ent in doc.ents if ent.label_ == 'CARDINAL']

if matching_trigrams==[('current', 'nba', 'season')]:
    doc = nlp('What team has the best record in the current NBA season?')
    year = [ent.text for ent in doc.ents if ent.label_ == 'DATE']

# If a player name is found, fetch the player's stats
if players:
    for player in players:
        first_name, last_name = player.split()
        player_id = NBA.get_player_ID_NBA(last_name, first_name)
        if player_id:
            if matching_bigrams ==[('career', 'stats')] :
                player_stats = NBA.get_nba_career_stats(player_id)
                print(f"NBA Response: {player_stats}")
            elif matching_bigrams == [('career','average')]:
                if matching_stats:
                    for stat in matching_stats:
                        player_stats=NBA.get_career_averages(player_id,stat)
                        print(player_stats)  
            elif matching_bigrams==[('play','for')]:
                player_stats = NBA.get_nba_career_stats(player_id)
                final_season=player_stats.iloc[-1]
                team_id=final_season['TEAM_ID']
                info=NBA.get_NBA_team_details(team_id)
                print(info)

            elif awards:
                for trophy in awards:
                    if trophy=='mvp':
                        if matching_words:
                            for word in matching_words:
                                if word == 'finals':
                                    player_award=NBA.get_player_award(player_id,'NBA Finals Most Valuable Player')
                                    if player_award:
                                        print (player_award)
                                    else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                        elif matching_bigrams:
                            for bigrams in matching_bigrams:
                                if bigrams==('all','star'):
                                    player_award=NBA.get_player_award(player_id,'NBA All-Star Most Valuable Player')
                                    if player_award:
                                        print (player_award)
                                    else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                elif bigrams==('sporting','news'):
                                    player_award=NBA.get_player_award(player_id,'NBA Sporting News Most Valuable Player of the Year')
                                    if player_award:
                                        print (player_award)
                                    else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                elif bigrams==('in','season'):
                                    player_award=NBA.get_player_award(player_id,'NBA In-Season Most Valuable Player')
                                    if player_award:
                                        print (player_award)
                                    else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                        else:
                            player_award=NBA.get_player_award(player_id,'NBA Most Valuable Player')
                            if player_award:
                                        print (player_award)
                            else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')

                    elif trophy=='rookie':
                        if matching_bigrams:
                             for bigrams in matching_bigrams:
                                 if bigrams==('rookie','year'):
                                     player_award=NBA.get_player_award(player_id,'NBA Rookie of the Year')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                 elif bigrams==('rookie','month'):
                                     player_award=NBA.get_player_award(player_id,'NBA Rookie of the Month')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif trophy=='player':
                        if matching_bigrams:
                             for bigrams in matching_bigrams:
                                 if bigrams==('player','week'):
                                     player_award=NBA.get_player_award(player_id,'NBA Player of the Week')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                 elif bigrams==('player','month'):
                                     player_award=NBA.get_player_award(player_id,'NBA Player of the Month')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif trophy=='medal':
                         if matching_bigrams:
                             for bigrams in matching_bigrams:
                                 if bigrams==('bronze','medal'):
                                     player_award=NBA.get_player_award(player_id,'Olympic Bronze Medal')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                 elif bigrams==('sliver','medal'):
                                     player_award=NBA.get_player_award(player_id,'Olympic Silver Medal')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                                 elif bigrams==('gold','medal'):
                                     player_award=NBA.get_player_award(player_id,'Olympic Gold Medal')
                                     if player_award:
                                        print (player_award)
                                     else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
            elif matching_bigrams:
                for bigrams in matching_bigrams:
                    if bigrams==('in','season'):
                        for bigrams in matching_bigrams:
                            if bigrams==('all','tornament'):
                                player_award=NBA.get_player_award(player_id,'NBA In-Season Tournament All-Tournament')
                                if player_award:
                                        print (player_award)
                                else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif bigrams==('all','nba'):
                        player_award=NBA.get_player_award(player_id,'All-NBA')
                        if player_award:
                                        print (player_award)
                        else:
                                        print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif bigrams==('all','defense'):
                        player_award=NBA.get_player_award(player_id,'All-Defensive Team')
                        if player_award:
                            print (player_award)
                        else:
                            print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif bigrams==('all','rookie'):
                        player_award=NBA.get_player_award(player_id,'All-Rookie Team')
                        if player_award:
                            print (player_award)
                        else:
                            print(f'{first_name.capitalize()}{last_name.capitalize()}')
                    elif bigrams==('double','doubles'):
                        doub_doubs=NBA.get_player_game_logs(player_id,DD=True)
                        print(doub_doubs)
                    elif bigrams==('triple','doubles'):
                        doub_doubs=NBA.get_player_game_logs(player_id,TD=True)
                        print(doub_doubs)
        else:
            print(f"I'm sorry, I couldn't find stats for {player}.")
elif teams:
    stop_words = set(stopwords.words('english'))
    teams_without_stopwords = [' '.join(word for word in word_tokenize(team) if word not in stop_words) for team in teams]
    for team in teams_without_stopwords:
        team_id = NBA.get_team_id(team)
        if team_id:
            if matching_words or matching_bigrams:
                for words in matching_words:
                    if words=='roster':
                        if year:
                            for years in year:
                                test=NBA.get_NBA_team_roster(team_id,years)
                                print(test)
                        else:
                             test=NBA.get_NBA_team_roster(team_id)
                             print(test)
                for bigrams in matching_bigrams:
                    if bigrams == ('played','for') or ('plays','for'):
                        if year:
                            for years in year:
                                test=NBA.get_NBA_team_roster(team_id,years)
                                print(test)
                        else:
                             test=NBA.get_NBA_team_roster(team_id)
                             print(test)
            elif numbers:
                for bigrams in top_10_bigrams:
                    for number in numbers:
                        if bigrams==(number,'rebounds'):
                            reb=int(number)
                        if bigrams==(number,'assists'):
                            assist=int(number)
                        if bigrams==(number,'steals'):
                            steals=int(number)
                        if bigrams==(number,'blocks'):
                            blocks=int(number)
                        if bigrams==(number,'fouls'):
                            fouls=int(number)
                        if bigrams==(number,'turnovers'):
                            to=int(number)
                        if bigrams==(number,'points'):
                            points=int(number)
                for word in matching_words:
                    if word == 'wins':
                        w=True
                    if word == 'losses':
                        l=True
                if year:
                    for years in year:
                        test=NBA.get_team_schedule(team_id,years,W=w,L=l,REB=reb,AST=assist,STL=steals,TOV=to,BLK=blocks,PF=fouls,PTS=points)
                        with pd.option_context('display.max_rows', None):
                            print(test)
            else:
                info=NBA.get_NBA_team_details(team_id)
                print(info)
        else :
            print(f"Sorry, We are unable to find anything about {team}")
elif awards:
    for trophy in awards:
        if trophy == 'mvp':
            if year:
                for years in year:
                    championship=NBA.get_mvp(years)
                    print (championship)
elif year:
     if matching_bigrams==[('best', 'record')]:
        if matching_trigrams==[('current', 'nba', 'season')]:
            selected_year=2023
            standings=NBA.get_league_standings(selected_year,1)
            print(standings)
        else: 
            for years in year:
                standings=NBA.get_league_standings(years,1)
                print(standings)
     if matching_words:
         for words in matching_words:
             if words == 'finals' or 'champion' or 'championship':
                 for years in year:
                     championship=NBA.get_nba_championship_winner(years)
                     print (championship)
elif numbers:
    for number in numbers:
       if staters:
           for people in stat_people:
               leaders=NBA.league_leaders(number)
               print(leaders)

elif matching_bigrams:
        if matching_bigrams == [('all','time')]:
            alltimeleader=NBA.AllTimeLeaders()
            print(alltimeleader)
        if matching_bigrams==[('most','points')]:
                mostpoints=NBA.single_game_records()
                print(mostpoints)

else:
    print("I'm sorry, I don't understand that NBA query.")

