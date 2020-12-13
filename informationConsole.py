import vk_api

def main():
    login, password = 'mazion2014@yandex.ru', 'Sehsid21602damKlimenkov33Daniil!'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    #---------------------------------------------------------
    countPosts = 0
    countReposts = 0
    countLikes = 0
    countComments = 0
    directory = "Information"

    lines = [line.rstrip('\n') for line in open('ids.txt')]

    for i in range(len(lines)):
        nameFile = directory + '/' + lines[i] + ".txt"
        f = open(nameFile, "w")
        input_id = lines[i]
        vk = vk_session.get_api()

    #Имя, фамилия пользователя, тип аккаунта, день рождения, город и страна
        user_get = vk.users.get(user_ids=(input_id),fields=("bdate,city,country,education,connections,domain"))
        user_get = user_get[0]
        first_name = user_get['first_name']
        f.write('1. Имя пользователя: '+ first_name +'\n')
        last_name = user_get['last_name']
        f.write('2. Фамилия пользователя: '+ last_name +'\n')
        islosed = user_get['is_closed']
        if (islosed):
            f.write('3. Аккаунт закрытый' +'\n')
        else:
            f.write('3. Аккаунт открытый' +'\n')
        import datetime

        try:
            bdate = user_get['bdate']
            td = datetime.datetime.now().date()
            array_bd = bdate.split('.')
            bd = datetime.date(int(array_bd[2]), int(array_bd[1]), int(array_bd[0]))
            age_years = int((td - bd).days / 365.25)
            f.write('4. День рождения: {}. Полных лет: {} \n'.format(bdate,age_years))
        except:
            f.write('4. День рождения указан не полностью \n')

        try:
            universityName = user_get['university_name']
            f.write("5. Университет: " + universityName + '\n')
        except:
            f.write("5. Университет не указан \n")

        try:
            instagram = user_get['instagram']
            f.write("6. Инстаграм: " + instagram + '\n')
        except:
            f.write("6. Инстаграм не указан \n")

        try:
            country = user_get['country']['title']
            f.write('7. Страна пользователя: ' + country + '\n')
        except:
            f.write('7. Страна пользователя не указана\n')

        try:
            country = user_get['city']['title']
            f.write('8. Город пользователя: ' + country + '\n')
        except:
            f.write('8. Город пользователя не указан\n')

    #Количество друзей
        user_friend = vk.friends.get(user_id=(input_id))
        countFriend = user_friend['count']
        f.write('9. Количество друзей : '+ str(countFriend) + '\n')

    #Количество подписчиков и подписок
        user_getFollowers = vk.users.getFollowers(user_id=(input_id))
        subscribers = user_getFollowers['count']
        user_getSubscriptions = vk.users.getSubscriptions(user_id=(input_id),extended = 1)
        subscriptions = user_getSubscriptions['count']
        f.write('10. Количество подписчиков: '+ str(subscribers) + '\n')
        f.write('11. Количество подписок: '+ str(subscriptions) + '\n')

    #Статус пользователя
        status_get = vk.status.get(user_id=(input_id))
        statusOfUser = status_get['text']
        if (statusOfUser == ''):
            f.write('12. У пользователя не установлен статуса\n')
        else:
            try:
                f.write('12. У пользователя статус: {} \n'.format(statusOfUser))
            except:
                f.write('12. В статусе присутствуют символы \n')

    #Анализ стены
        f.write("13. Анализ стены: " + '\n')
        from datetime import datetime
        wall = tools.get_all('wall.get', 100, {'owner_id': input_id})
        for i in range(wall['count']):
            One = wall['items'][i]['from_id']
            Two = wall['items'][i]['owner_id']
            DateCount = wall['items'][i]['date']
            Date = (datetime.fromtimestamp(DateCount))
            Likes = wall['items'][i]["likes"]["count"]
            countLikes += Likes
            Comments = wall['items'][i]['comments']['count']
            countComments += Comments
            if (One == Two):
                f.write('Запись №{} является постом. {} лайк(-ов). {} комментариев. Дата {}\n'.format(i+1, Likes, Comments, Date))
                countPosts += 1
            else:
                f.write('Запись №{} является репостом или чужой записью. {} лайков. {} комментариев. Дата {}\n'.format(i+1, Likes, Comments, Date))
                countReposts += 1
        f.write("Общая информация:\n")
        rep = countPosts + countReposts
        f.write("Количество записей: " + str(rep) + '\n')
        f.write("Количество постов: " + str(countPosts) + '\n')
        f.write("Количество репостов: " + str(countReposts) + '\n')
        f.write("Количество лайков: " + str(countLikes) + '\n')
        f.write("Количество комментов: " + str(countComments) + '\n')

        print("С пользоваталем {} закончили".format(input_id))

if __name__ == '__main__':
    main()

