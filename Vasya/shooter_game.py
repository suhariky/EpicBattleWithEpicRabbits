#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def  __init__(self, player_image, xcor, ycor, widht, height, speed, speed2):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (widht, height))
        self.speed = speed
        self.speed2 = speed2
        self.rect = self.image.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < 395:
            self.rect.y += self.speed

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 35, 35, -20, 0)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        switch = randint(0, 11)
        if switch % 2 == 0:
            direction = "left"

        else:
            direction = "right"

        if direction == "left":
            self.rect.y += self.speed
            self.rect.x -= self.speed2

        else:
            self.rect.y += self.speed
            self.rect.x += self.speed2

        global lost
        if self.rect.y > 450:
            self.rect.x = randint(80, 620)
            self.rect.y = randint(-5, 0)
            lost += 1
            self.speed = randint(1, 12)
            self.speed2 = randint(1, 12)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font_stat = font.SysFont("Arial", 36)
font_end = font.SysFont("Arial", 80)
lose_font = font_end.render("YOY DЭD", True, (200, 25, 25))
win_font = font_end.render("YOY WИN", True, (25, 200, 25))

mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play(loops=-1)
shot = mixer.Sound("fire.ogg")
#lose = mixer.Sound("lose.ogg")

window = display.set_mode((700,500))
background = transform.scale(image.load("Divasyo.jpg"), (700,500))

timer = time.Clock()
finish = False
game = True
lost = 0
score = 0
max_score = 10
life_points = 5

player_image = "Vasya.JPG"
asteroid_image = "superEnemy.JPG"
enemy_image = "Lisa.JPG"
bullet_image = "morkovkaaaa.png"

player = Player(player_image, 5, 400, 80, 100, 18, 0)
enemies = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 8):
    enemy = Enemy(enemy_image, randint(5,680), randint(5,150), 80, 70, 3, 3)
    enemies.add(enemy)

for i in range(1,7):
    asteroid = Enemy(asteroid_image, randint(5,680), randint(5,150), 70, 70, 5, 5)
    asteroids.add(asteroid)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #shot.play()
                player.fire()
            
    if not finish:        
        window.blit(background, (0,0))
        text_win = font_stat.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text_win, (10, 20))
        text_lose = font_stat.render("Пропущено " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if sprite.groupcollide(bullets, asteroids, True, True) or sprite.groupcollide(bullets, enemies, True, True):
            score += 1

        player.update()
        enemies.update()
        asteroids.update()
        bullets.update()

        player.reset()
        enemies.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            life_points -= 1
            if life_points <= 0:
                window.blit(lose_font, (200, 200))
                finish = True
        
        if score >= max_score:
            finish = True
            window.blit(win_font, (200, 200))

        text_life = font_stat.render("Жизни: " + str(life_points), 1, (255, 255, 255))
        window.blit(text_life, (560, 20))

        display.update()

    else:
        life_points = 5
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()

        for e in enemies:
            e.kill()

        for a in asteroids:
            a.kill()

        time.delay(300)

        for i in range(1,7):
            asteroid = Enemy(asteroid_image, randint(5,680), randint(5,150), 70, 70, 5, 5)
            asteroids.add(asteroid)

        for i in range(1, 8):
            enemy = Enemy(enemy_image, randint(5,680), randint(5,150), 80, 70, 3, 3)
            enemies.add(enemy)



    time.delay(50)