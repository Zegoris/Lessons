import vk_api, time
from flask import Flask, render_template

"""LOGIN, PASSWORD = input('Login: '), input('Password: ')"""


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


def main():
    """login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    response = vk.stats.get(group_id=GROUP_ID, fields='reach', intervals_count=10)
    if response:
        information = dict()
        information['Activities'] = [('likes', response['activity']['likes']),
                                     ('comments', response['activity']['comments']),
                                     ('subscribed', response['activity']['subscribed'])]
        information['Ages'] = response['reach']['age']
        information['Cities'] = [i['name'] for i in response['reach']['cities']]
    else:
        exit()"""
    information = {'Activities': [('likes', 1), ('comments', 5), ('subscribed', 10)],
                   'Ages': [('12-18', 1), ('18-21', 5)],
                   'Cities': ['Moscow, Russia']}
    app = Flask(__name__)

    @app.route('/')
    def init():
        return render_template('main.html')
    @app.route('/vk_stat/<int:group_id>')
    def statistic(group_id):
        """login, password = LOGIN, PASSWORD
        vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        vk = vk_session.get_api()
        response = vk.stats.get(group_id=group_id, fields='reach', intervals_count=10)
        if response:
            information = dict()
            information['Activities'] = [('likes', response['activity']['likes']),
                                         ('comments', response['activity']['comments']),
                                         ('subscribed', response['activity']['subscribed'])]
            information['Ages'] = response['reach']['age']
            information['Cities'] = [i['name'] for i in response['reach']['cities']]
        else:
            exit()"""
        return render_template('stats.html', info=information)

    app.run(port=5050, host='127.0.0.1')





if __name__ == '__main__':
    main()