
from flask import Flask, request, jsonify
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}
second = False

@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    global second
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:
        if not second:
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!\nПривет! Купи кролика!'

        else:
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
            res['response']['end_session'] = True
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        second = True
        return

    if not second:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
        res['response']['buttons'] = get_suggests(user_id)
    else:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"
        res['response']['buttons'] = get_suggests(user_id)

def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if not second:
        if len(suggests) < 2:
            suggests.append({"title": "Ладно",
                             "url": "https://market.yandex.ru/search?text=слон",
                             "hide": True
                             })
    else:
        if len(suggests) < 2:
            suggests.append({"title": "Ладно",
                             "url": "https://market.yandex.ru/search?text=кролик",
                             "hide": True
                             })
    return suggests


if __name__ == '__main__':
    app.run()