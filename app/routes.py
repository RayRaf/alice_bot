import json
import random, string
from datetime import datetime
from flask import current_app, request, jsonify

# Загружаем команды и ответы из внешнего файла
with open('responses.json', 'r', encoding='utf-8') as f:
    RESPONSES = json.load(f)
    print("Содержимое JSON-файла:", RESPONSES)

# Логика обработки запросов

@current_app.route('/webhook', methods=['POST'])
def webhook():
    req = request.json
    user_request = req['request']['command'].lower().strip()

    if user_request.startswith("алиса "):
        user_request = user_request[len("алиса "):]

    # Удаляем знаки препинания
    user_request = user_request.translate(str.maketrans("", "", string.punctuation))

    print(f"Получена команда после очистки: '{user_request}'")

    end_session = False
    response_text = "Я че то не догоняю. Повтори а то не расслышал."

    # Логика обработки команды "Когда идем играть в теннис?"
    tennis_phrases = [
        "когда идем играть в теннис",
        "когда пойдем играть в теннис",
        "во сколько играем в теннис",
        "пойдем ли сегодня играть в теннис",
        "когда рубилово"
    ]

    if any(phrase in user_request for phrase in tennis_phrases):
        # Текущее время
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Целевое время 12:00
        target_hour = 12
        target_minute = 0

        # Разница во времени
        hours_diff = target_hour - current_hour
        minutes_diff = target_minute - current_minute

        # Если разница в минутах отрицательная, компенсируем сдвиг времени
        if minutes_diff < 0:
            minutes_diff += 60
            hours_diff -= 1

        # Если время уже прошло, добавляем 24 часа
        if hours_diff < 0:
            hours_diff += 24

        # Формируем ответ
        response_text = (f"Наказывать всех в теннисе пойдем через "
                         f"{hours_diff} часов {minutes_diff} минут.")

    elif "привет" in user_request:
        response_text = "Привет, как я могу помочь?"

    elif "скажи комплимент" in user_request:
        response_text = """Анастасия Владимировна, золотая наша..."""

    elif user_request in {key.lower(): key for key in RESPONSES.get("комплименты", {})}:
        response_text = random.choice(RESPONSES["комплименты"][
            {key.lower(): key for key in RESPONSES.get("комплименты", {})}[user_request]
        ])

    elif user_request in {key.lower(): key for key in RESPONSES.get("прочие", {})}:
        response_text = RESPONSES["прочие"][
            {key.lower(): key for key in RESPONSES.get("прочие", {})}[user_request]
        ]
                
    return jsonify({
        "version": req['version'],
        "session": req['session'],
        "response": {
            "text": response_text,
            "end_session": end_session
        }
    })
