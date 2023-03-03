import vk_api, time

LOGIN, PASSWORD = input('Login: '), input('Password: ')
ALBUM_ID, GROUP_ID = input('Album id: '), input('Group id: ')


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    upload = vk_api.VkUpload(vk_session)
    photos = upload.photo(['static/img/photo1.jpeg',
                          'static/img/photo2.jpeg',
                          'static/img/photo3.jpeg'],
                         album_id=ALBUM_ID, group_id=GROUP_ID)

    vk = vk_session.get_api()
    vk.wall.post(message="Test", attachments=[f"photo{i['owner_id']}_{i['id']}" for i in photos])



if __name__ == '__main__':
    main()