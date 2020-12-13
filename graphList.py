import vk_api
import networkx as nx
import time

def main():
    login, password = 'mazion2014@yandex.ru', 'Sehsid21602damKlimenkov33Daniil!'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    def nameFromId(id):
        user_get = vk.users.get(user_ids=(id))
        user_get = user_get[0]
        first_name = user_get['first_name']
        last_name = user_get['last_name']
        name = (str(first_name) + " " + str(last_name))
        return name

    start = time.time()
    vk = vk_session.get_api()
    g = nx.Graph(directed=False)
    listUsers = []

    lines = [line.rstrip('\n') for line in open('ids.txt')]
    for i in range(len(lines)):
        temp = lines[i]
        temp = str(temp)
        listUsers.append(temp)

    for i in range(len(listUsers)):
        count = 0
        listFriend = []
        commonFriends = []
        user_friend = vk.friends.get(user_id=(listUsers[i]), fields=('domain'))
        countFriend = user_friend['count']

        for j in range(countFriend):
            listFriend.append(str(user_friend['items'][j]['id']))

        for k in listUsers:
            for l in listFriend:
                if k == l:
                    commonFriends.append(k)
                    break
        count = len((commonFriends))

        node = listUsers[i]
        g.add_node(node)
        print('User -', node)
        for j in range(len(commonFriends)):
            if (listUsers[i] != commonFriends[j]):
                g.add_edge(listUsers[i], commonFriends[j])

    print('Время выполнения', round((time.time() - start), 2), 'секунд')
    nx.write_graphml(g, "test.graphml")

if __name__ == '__main__':
    main()

