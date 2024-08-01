import requests
from datetime import date

def find_matches():
    print('zapros')
    # Список интересующих лиг
    leagues = ["235", "123"]

    # Дата сегодняшнего дня
    today = date.today().strftime("%Y-%m-%d")

    matches = []

    for league_id in leagues:
        url = "https://v3.football.api-sports.io/fixtures"
        querystring = {
            "league": league_id,
            "season": "2024",
            "date": today
        }
        headers = {
            'x-apisports-key': "d687e02afc3ddcaf9299988a94faf74f"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        for fixture in data['response']:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            fixture_id = fixture['fixture']['id']

            match_data = get_match_data(home_team, away_team, fixture_id)
            matches.append(match_data)

    return matches

def get_match_data(home_team, away_team, fixture_id):
    url = "https://v3.football.api-sports.io/predictions"
    querystring = {
        "fixture": fixture_id  # Здесь нужно указать ID матча
    }
    headers = {
        'x-apisports-key': "d687e02afc3ddcaf9299988a94faf74f"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    match_data = {
        "home_team": home_team,
        "away_team": away_team,
        "fixture_id": fixture_id,
        "prediction_data": []
    }

    for prediction in data['response']:
        advice = prediction["predictions"]['advice']
        home_team_percent = prediction["predictions"]['percent']['home']
        home_team_last_5_avg_goals = prediction['teams']['home']['last_5']['goals']['for']['average']
        home_team_last_5_against_avg_goals = prediction['teams']['home']['last_5']['goals']['against']['average']

        away_team_percent = prediction["predictions"]['percent']['away']
        away_team_last_5_avg_goals = prediction['teams']['away']['last_5']['goals']['for']['average']
        away_team_last_5_against_avg_goals = prediction['teams']['away']['last_5']['goals']['against']['average']

        draw_percent = prediction["predictions"]['percent']['draw']

        match_data['prediction_data'].append({
            "advice": advice,
            "home_team_percent": home_team_percent,
            "home_team_last_5_avg_goals": home_team_last_5_avg_goals,
            "home_team_last_5_against_avg_goals": home_team_last_5_against_avg_goals,
            "away_team_percent": away_team_percent,
            "away_team_last_5_avg_goals": away_team_last_5_avg_goals,
            "away_team_last_5_against_avg_goals": away_team_last_5_against_avg_goals,
            "draw_percent": draw_percent
        })

    return match_data


def get_odds(fixture_id):
    url = "https://v3.football.api-sports.io/odds"
    querystring = {
        "fixture": fixture_id,
        "bookmaker": "11"
    }
    headers = {
        'x-apisports-key': "d687e02afc3ddcaf9299988a94faf74f"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    message = ""

    for odd in data['response']:
        for bookmaker in odd['bookmakers']:
            if bookmaker['name'] == '1xBet':
                for bet in bookmaker['bets']:
                    if bet['name'] == 'Home Team Yellow Cards':
                        for value in bet['values']:
                            num_odd = float(value['odd'])
                            if 1.3 <= num_odd <= 2.2:
                                bet_type, bet_indx = value['value'].split(' ')
                                if int(bet_indx[-1]) == 5 and len(bet_indx) == 3:
                                    message += f"Тотал 1 команды: {bet_type} {bet_indx} за {num_odd}\n"

                    elif bet['name'] == 'Away Team Yellow Cards':
                        for value in bet['values']:
                            num_odd = float(value['odd'])
                            if 1.3 <= num_odd <= 2.2:
                                bet_type, bet_indx = value['value'].split(' ')
                                if int(bet_indx[-1]) == 5 and len(bet_indx) == 3:
                                    message += f"Тотал 2 команды: {bet_type} {bet_indx} за {num_odd}\n"

                    elif bet['name'] == 'Yellow Over/Under':
                        for value in bet['values']:
                            num_odd = float(value['odd'])
                            if 1.3 <= num_odd <= 2.2:
                                bet_type, bet_indx = value['value'].split(' ')
                                if int(bet_indx[-1]) == 5 and len(bet_indx) == 3:
                                    message += f"Общий Тотал: {bet_type} {bet_indx} за {num_odd}\n"

                    elif bet['name'] == 'Yellow Cards 1x2':
                        for value in bet['values']:
                            num_odd = float(value['odd'])
                            if 1.1 <= num_odd:
                                bet_type = value['value']
                                if bet_type != "Draw":
                                    message += f"Cards 1x2: {bet_type} за {num_odd}\n"

    return message
