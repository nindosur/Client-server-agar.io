# Server
import random
import socket
from threading import Thread

# Цвета кружочков
color_cells = [(80, 252, 54),
               (36, 244, 255),
               (243, 31, 46),
               (4, 39, 243),
               (254, 6, 178),
               (255, 211, 7),
               (216, 6, 254),
               (146, 255, 7),
               (7, 255, 182),
               (255, 6, 86),
               (177, 7, 255)]

# Игровое поле - массив с ячейка
dots = {j:{'X': random.randint(20, 2000), 'y': random.randint(20, 2000),
        'color': color_cells[random.randint(0, len(color_cells)-1)]} for j in range(2000)}

# Список пользователей
all_users = {}
# Функция рассылки обновления карты
def upd_eaten(dots, all_users):
    eaten_dots_ids = []                         # массив съеденных точек
    for i, dot in dots.items():
        for name, user in all_users.items():
            # проверка на то, была ли съедена точка пользователем
            if ((dot['x'] - user['x'])**2+ (dot['y'] - user['y']**2)**0.5 <= user['mass']/2):
                all_users[name]['mass'] += 0.5  # если съедена - массу игрока увиличиваем
                eaten_dots_ids.append(i)        # точку записываем в массив съеденных
    for dot in eaten_dots_ids:                  # удаляем из массива все съеденные точки
        del dots[dot]
    return eaten_dots_ids                       # возвращаем массив съеденных точек

# Функция для подключения новых игроков
def on_new_client(clientsocket, addr):
    while True:                                         # бесконечный цикл ожидания подключения к серверу игроков
        msg = clientsocket.recv(1024)
        # print(addr, '>>>', msg)
        if msg == b'close':                             # сообщение о закрытии подключения = выход из цикла
            break
        if msg == b'spawn':                             # сообщение о спавне = отправка игроку массива точек
            msg = bytes(str(dots), encoding='utf-8')
            clientsocket.sendall(msg)
            print('sent dots')
        else: # если сообщение другое = добавим имя пользователя в массив пользователей, отправим список съеденных точек
            user = eval(msg.decode('utf-8'))
            all_users[user['name']] = user
            eaten_dots_ids = upd_eaten(dots, all_users)
            resp = {'user': all_users[user['name']], 'eaten_dots_ids': eaten_dots_ids}
            msg = bytes(str(resp), encoding='utf-8')
            clientsocket.send(msg)
    clientsocket.close()

# Работа с сервером
host = 'localhost'              # адрес сервера
port = 34325                    # порт сервера
server_adress = (host, port)    # константа
s = socket.socket()             # создание объекта сокета
s.bind(server_adress)           # вкл. сервера
s.listen(10)                    # режим ожидания сообщения к серверу (прослушка)
print('Server started')
print('Waiting for clients...')

try:
    while True:
        c, addr = s.accept()
        print(f'Got connection from {addr}')
        thead = Thread(target= on_new_client, args=(c, addr))
        thead.start()
except KeyboardInterrupt:
    s.close()
    print('Server closed')