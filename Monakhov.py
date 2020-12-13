# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
name = []
import vk_api
import networkx as nx
def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True
    return key, remember_device


def get_friend_ids(tools, id):
    friends = tools.get_all('friends.get', 5000, {'user_id': id})
    return friends['items']

def get_friend_names(tools, name):
    friends = tools.get_all('friends.get', 5000, {'user_name': name})
    return friends['items']

def get_name(vk,id):
    user_get = vk.users.get(user_ids=(id))
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']
    name = first_name + last_name
    return name


def main():
    """ Пример обработки двухфакторной аутентификации """

    login, password = 'mazion2014@yandex.ru', 'Sehsid21602damKlimenkov33Daniil!'
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    friend_ids = get_friend_ids(tools, 551289635)  # ваш user id, для которого вы хотите построить граф друзей.

    vk = vk_session.get_api()

    g = nx.Graph(directed=False)
    g.add_nodes_from(friend_ids)
    for friend_id in friend_ids:
        g.add_edge(551289635, friend_id)
        try:
            name = get_name(vk, friend_id)
            print('Processing id: ', name)
            for f_id in get_friend_ids(tools, friend_id):
                g.add_node(name)
                g.add_edge(friend_id, f_id)
        except:
            print('Access denied for user #', name)
    nx.write_graphml(g, "g.graphml")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
