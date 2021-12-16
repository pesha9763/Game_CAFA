import pygame
import math

"""для начала было бы неплохо написать
всю разметку там, обозначить границы карты
и сделать остальную рутину"""
"""размер окна"""
win_sx = 20  # количество квадратов по икс
win_sy = 20  # по игрек
side_s = 30  # сторона

width = win_sx * side_s + 1
height = win_sy * side_s + 1
fps = 30

red = (255, 0, 0)
dark_red = (155, 0, 0)
green = (0, 255, 0)
dark_green = (0, 155, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 155)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

pygame.init()

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tower defence")  # подпись
clock = pygame.time.Clock()

"""функция отрисовки карты чтобы разделить ее на 
    равные клетки"""


def draw_wind():
    """добавим отображение на какую клетку указывает курсор"""
    mp = pygame.mouse.get_pos()
    x = math.floor(mp[0] / side_s) * side_s
    y = math.floor(mp[1] / side_s) * side_s
    pygame.draw.rect(win, dark_blue, [x, y, side_s, side_s])
    """отрисовываем линии на равном расстоянии"""
    for Line in range(win_sx + 1):
        pygame.draw.line(win, dark_green, [Line * side_s, 0], [Line * side_s, height * side_s])
    for Line in range(win_sy + 1):
        pygame.draw.line(win, dark_green, [0, Line * side_s], [width, Line * side_s])
    for line in range(win_sx):
        pygame.draw.line(win, dark_green, [line * side_s, 0], [line * side_s, height * side_s])


class tower:  # создаем класс башни
    """метод класса для отрисовки башни с необхимыми параметрами"""

    def __init__(self, x, y, size, color, damage, fire):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage  # урон который башня наносит врагу
        self.fire = fire  # время через которое летит следующая пуля
        self.fire_time = 0  # типа таймер

    """функция котооая ставит башню по нажатию на пробел"""

    def draw(self):
        pygame.draw.circle(win, self.color, [self.x, self.y], self.size)

    """округляя в меньшую сторону координаты мыши узнаем
    квадрат на который указываем"""

    """тестовый метод стрельбы: 
        пули будут лететь вверх - это вектор 0, -1"""

    def shoot(self):
        # put_w(self.x, self.y, 3, white, 5, 3)
        """добавим задержку чтобы пули не летели подряд"""
        if self.fire_time <= 0:
            put_w(self.x, self.y, 10, white, 2, 3)
            self.fire_time = self.fire
        else:
            self.fire_time -= 1 / fps


towers = []


def put_t():
    mp = pygame.mouse.get_pos()
    x = math.floor(mp[0] / side_s) * side_s
    y = math.floor(mp[1] / side_s) * side_s
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and tow_ok(x, y):
        towers.append(tower(x + side_s / 2, y + side_s / 2, 10, yellow, 5, 2))
        """учитывая что башня ставится в центр квадрата, 
        прибавляем к координате половину длины стороны клетки"""


"""башни должны в кого то стрелять поэтому аналогично создвем врагов"""


class enemy:
    def __init__(self, x, y, size, color, heal, fast):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.heal = heal  # сколько может выдержать
        self.fast = fast
        self.dot = 0


    def draw(self):
        pygame.draw.circle(win, self.color, [self.x, self.y], self.size)
    """создадим метод для движения по дотам"""
    def go_en(self):
        go = fcnmath(self.x, check[self.dot][0], self.y, check[self.dot][1])
        self.x += self.fast * go[0]
        self.y += self.fast * go[1]
        if go[2] <= self.fast:
            self.dot += 1
            if self.dot == len(check):
                enem.remove(self)


enem = []


def put_e(size, color, heal, fast):
    """создадим 10 неподвижных врагов
    for i in range(10):
        enem.append(enemy(i * side_s + side_s / 2, 6 * side_s + side_s / 2, 15, red, 10, 10))"""
    for i in range(10):
        x = check[0][0] - 200 - i*10 - 5
        y = check[0][1]
        enem.append(enemy(x, y, size, color, heal, fast))


"""нам нужна башня которая чем то стреляет
создадим класс для снарядов/пуль"""


class weapon:
    """из параметров: координаты создания, скорость, цвет,
    урон который несет пуля
    а еще метод для отрисовки и движения"""

    def __init__(self, x, y, speed, col, death, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.col = col
        self.death = death
        self.size = size

    def draw(self):
        pygame.draw.circle(win, self.col, [self.x, self.y], self.size)

    def go(self, nx_v, ny_v):
        self.x += nx_v * self.speed
        self.y += ny_v * self.speed


"""список для хравния и функция создания"""
weapons = []


def put_w(x, y, speed, col, death, size):
    weapons.append(weapon(x, y, speed, col, death, size))


"""чтобы пули летели во врага нужно заморочиться с математикой"""


def fcnmath(x1, x2, y1, y2):
    x_v = x2 - x1
    y_v = y2 - y1
    d = math.hypot(x_v, y_v)
    nx_v = x_v / d
    ny_v = y_v / d
    a = math.atan2(ny_v, nx_v)
    return nx_v, ny_v, d, a


"""чтобы башни не совпадали и не ставились друг на друга
сделаю следующее"""


def tow_ok(x, y):
    x += side_s / 2
    y += side_s / 2
    if len(towers) != 0:
        for tower in towers:
            if tower.x == x and tower.y == y:
                return False
    for step in road:
        if step[0] + side_s/2 == x and step[1] + side_s/2 == y:
            return False
    return True


"""def tow_on_r(x,y):
    for step in road:
        if step[0] + side_s/2 == x and step[1] + side_s/2 == y:
            return False
    return True"""

"""создадим поле игры
в ней 0 это простое поле а 1  это то где враг будет идти"""

field = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
]

road = []

"""хранит данные о клетке карты и заполняет ее"""


def do_r():
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] > 0:  # запретим ставить башни на дороге
                road.append([j * side_s, i * side_s, side_s, side_s])


def put_r(col):
    for x in road:
        pygame.draw.rect(win, col, x)


"""создадим функцию которая поможет врагу двигаться
на каждом повороте будет точка к которой надо приблизиться"""


check = []


def checkpoin(count):
    dot = 2
    for x in range(count):
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == dot:
                    check.append([j * side_s + side_s/2, i * side_s + side_s/2])
                    dot += 1
                    """надо в углы карты написать цифры начиная с 2"""


def death_check():
    for enemy in enem:
        if enemy.heal <= 0:
            enem.remove(enemy)



def main():
    draw_wind()
    put_t()
    put_r(white)
    """for steps in check:
        pygame.draw.rect(win, black, steps)"""
    for tower in towers:
        tower.draw()
        tower.shoot()
    for enemy in enem:
        enemy.draw()
        enemy.go_en()
    death_check()
    for weapon in weapons:
        a = fcnmath(weapon.x, enem[0].x, weapon.y, enem[0].y)  # самый первый враг
        weapon.go(a[0], a[1])
        """уничтожение пули и урон врагу"""
        if a[2] <= weapon.speed:
            enem[0].heal -= weapon.death
            weapons.remove(weapon)
        weapon.draw()
    death_check()


do_r()
checkpoin(8)
put_e(10, red, 10, 3)
# print(check)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        win.fill(black)
        #put_e()
        main()
        pygame.display.update()
        clock.tick(fps)

pygame.quit()
