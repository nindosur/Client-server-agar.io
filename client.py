# Client
import random
import math
import socket
import pygame

    # Инициализируем библиотеку pygame
pygame.init()
    # Массив цветов игоров
colors_players = [(37, 7, 255),
               (35, 183, 253),
               (48, 254, 242),
               (19, 79, 251),
               (255, 7, 230),
               (255, 7, 23),
               (6, 254, 13)]
    # Цвета шаров
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

    # Цвета вирусов
color_virus = [(66, 254, 71)]

screen_width, screen_height = (800, 480)    # ширина и высота
surface = pygame.display.set_mode((screen_width, screen_height))    # поле для отрисовки объектов
pygame.display.set_caption('Agar.io')       # заголовок экрана
cell_list = list()                          # список ячеек
clock = pygame.time.Clock()                 # таймер для установки пауз в игре
font = pygame.font.Font(None, 20)           # шрифт



def draw_grid(camera):
    for i in range(0, 2001, 25):
        pygame.draw.line(surface, (230, 240, 240), (0+camera.x, i*camera.zoom+camera.y),
                         (2001*camera.zoom + camera.x, i*camera.zoom+camera.y), 3)
        pygame.draw.line(surface, (230, 240, 240), (i*camera.zoom+camera.x, 0 + camera.y),
                         (i*camera.zoom+camera.x, 2001*camera.zoom+camera.y), 3)

# Класс игрок
class Player:
    def __init__(self, surf, name='', x=random.randint(100,400), y=random.randint(100,400), mass=20, color=colors_players[random.randint(0, len(colors_players)-1)]):
        self.startX = self.x = x
        self.startY = self.y = y
        self.mass = mass
        self.surf = surf
        self.color = color
        self.name = name
    @property
    def info(self):
        return {'x': self.x, 'y': self.y, 'color': self.color, 'mass': self.mass, 'name': self.name}
    def move(self):
        dX, dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY - (float(screen_height)/2),
                              dX - (float(screen_width)/2))*180/math.pi
        speed = 4
        vx = speed*(90-math.fabs(rotation))/90
        vy = 0
        if rotation < 0:
            vy = -speed + math.fabs(vx)
        else:
            vy = speed - math.fabs(vx)
        self.x += vx
        self.y += vy
    def draw(self, cam):
        col = self.color
        zoom = cam.zoom
        x = cam.x
        y = cam.y
        pygame.draw.circle(self.surf, (col[0]-int(col[0]/3),
                                       int(col[1]-col[1]/3),
                                       int(col[2]-col[2]/3)),
                           (int(self.x*zoom+x), int(self.y*zoom+y)),
                           int((self.mass/2+3)*zoom))
        pygame.draw.circle(self.surf, col, (int(self.x*cam.zoom+cam.x),
                                            (int(self.y*cam.zoom+cam.y)),
                                            int(self.mass/2*zoom)))
        if len(self.name) > 0:
            fw, fh = font.size(self.name)
            drawText(self.name, (self.x*cam.zoom + cam.x -
                     int(fw/2), self.y*cam.zoom + cam.y -
                     int(fh/2)), (50, 50, 50))

class Cell:
    def __init__(self, surf, x, y, color=color_cells[random.randint(0, len(color_cells)-1)]):
        self.x = x
        self.y = y
        self.mass = 7
        self.surface = surf
        self.color = color

    def draw(self, cam):
        pygame.draw.circle(self.surface, self.color,
                           (int((self.x*cam.zoom+cam.x)),
                           int(self.y*cam.zoom+cam.y)),
                           int(self.mass*cam.zoom))

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = screen_width
        self.height = screen_height
        self.zoom = 0.5

    def centre(self, blobOrPos):
        if isinstance(blobOrPos, Player):
            p = blobOrPos
            self.x = (p.startX - (p.x*self.zoom)) - p.startX + screen_width/2
            self.y = (p.startY - (p.y*self.zoom)) - p.startY + screen_height/2
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos


# Вывод надписей на экран
def draw_text(message, pos, color=(255, 255, 255)):
    surface.blit(font.render(message, 1, color), pos)

# if __name__ == '__main__':
#     # Инициализируем библиотеку pygame
#     pygame.init()
#     # Массив цветов игоров
#     colors_players = [(37, 7, 255),
#                       (35, 183, 253),
#                       (48, 254, 242),
#                       (19, 79, 251),
#                       (255, 7, 230),
#                       (255, 7, 23),
#                       (6, 254, 13)]
#     # Цвета шаров
#     color_cells = [(80, 252, 54),
#                    (36, 244, 255),
#                    (243, 31, 46),
#                    (4, 39, 243),
#                    (254, 6, 178),
#                    (255, 211, 7),
#                    (216, 6, 254),
#                    (146, 255, 7),
#                    (7, 255, 182),
#                    (255, 6, 86),
#                    (177, 7, 255)]
#
#     # Цвета вирусов
#     color_virus = [(66, 254, 71)]
#
#     screen_width, screen_height = (800, 480)  # ширина и высота
#     surface = pygame.display.set_mode((screen_width, screen_height))  # поле для отрисовки объектов
#     pygame.display.set_caption('Agar.io')  # заголовок экрана
#     cell_list = list()  # список ячеек
#     clock = pygame.time.Clock()  # таймер для установки пауз в игре
#     font = pygame.font.Font(None, 20)  # шрифт


curr_user_name = input('Enter name: ')

address_to_server = ('localhost', 34325)
client = socket.socket()
client.connect(address_to_server)

camera = Camera()
blob = Player(surface, curr_user_name)

client.send(bytes('spawn', encoding='utf-8'))
cells = ''
while True:
    r = client.recv(1024).decode('UTF-8')
    cells = cells + r
    if r[-2:] == '}}':
        break
cells = eval(cells)
cells = {k :Cell(surface, v['x'], v['y'], v['color']) for k, v in cells.items()}

print('Start_game')

while True:
    clock.tick(70)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN or e.type == pygame.QUIT:
            client.send(bytes('close', encoding='utf-8'))
            client.close()
            print('end game')
            pygame.quit()
            quit()
    blob.move()
    client.send(bytes(str({'name':blob.name, 'x':blob.x, 'y':blob.y, 'mass':blob.mass}), encoding='utf-8'))
    r = eval(client.recv(1024).decode('UTF-8'))
    dots2drop = r['eaten_dots_ids']
    blob_info = r['user']
    blob_mass = blob_info['mass']
    for d in dots2drop:
        del cells[d]
    camera.zoom = 100/blob_mass + 0.3
    camera.centre(blob)
    surface.fill((242, 252, 255))
    draw_grid(camera)
    for i, c in cells.items():
        c.draw(camera)
    blob.draw(camera)
    pygame.display.flip()








