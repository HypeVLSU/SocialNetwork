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

    def countFriend(id):
        user_friend = vk.friends.get(user_id=(id))
        count = user_friend['count']
        return count

    def arrayFriend(id):
        nameUser = []
        user_friend = vk.friends.get(user_id=(id),fields=('domain'))
        count = user_friend['count']

        for i in range(count):
            temp1 = user_friend['items'][i]['first_name']
            temp2 = user_friend['items'][i]['last_name']
            nameUser.append(str(temp1) + " " + str(temp2))

        return nameUser

    start = time.time()
    vk = vk_session.get_api()
    id_user = 551289635
    nameMainUser = nameFromId(id_user)
    user_friend = vk.friends.get(user_id=(id_user),fields=('domain'))
    countFriendMainUser = user_friend['count']
    arrayFriendMainUser = []

    for i in range(countFriendMainUser):
        arrayFriendMainUser.append(user_friend['items'][i]['id'])

    nameFriendMainUser = arrayFriend(id_user)

    g = nx.Graph(directed=False)
    g.add_node(nameMainUser)

    for i in range(countFriendMainUser):
        g.add_node(nameFriendMainUser[i])
        g.add_edge(nameMainUser, nameFriendMainUser[i])

    print('С главным профилем закончили. Начинаем с друзьями. Их:', len(nameFriendMainUser))

    for i in range(len(arrayFriendMainUser)):
        idNewOffUser = arrayFriendMainUser[i]
        nameOffFriend = nameFromId(idNewOffUser)
        try:
            countFriendOffUser = countFriend(idNewOffUser)

            print('Работаем с профилем {}. Количество друзей - {}.'.format(idNewOffUser, countFriendOffUser))

            nameFriendOffUser = arrayFriend(idNewOffUser)

            for i in range(countFriendOffUser):
                g.add_node(nameFriendOffUser[i])
                g.add_edge(nameOffFriend, nameFriendOffUser[i])
        except:
            print("Профиль {} является закрытым".format(idNewOffUser))

    print('Время выполнения', round((time.time() - start), 2), 'секунд')
    nx.write_graphml(g, "test.graphml")

if __name__ == '__main__':
    main()

