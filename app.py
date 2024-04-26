from flask import Flask, render_template
import worker

app = Flask(__name__)

# Переменная для хранения флага, были ли сегодняшние матчи запрошены впервые
matches_requested = False

# Переменная для хранения данных о матчах
matches_data = []

@app.route('/')
def index():
    global matches_requested
    global matches_data

    # Если сегодняшние матчи еще не были запрошены, отправляем запрос на сайт
    if not matches_requested:
        matches_data = worker.find_matches()
        if matches_data:
            matches_requested = True

    print(matches_data)
    # Получение данных о матчах
    if matches_data:
        return render_template('matches.html', matches=matches_data)
    else:
        return "На сегодняшний день нет матчей."


@app.route('/stats/<int:fixture_id>')
def match_stats(fixture_id):
    stats = worker.get_odds(fixture_id)
    return stats


if __name__ == '__main__':
    app.run()
