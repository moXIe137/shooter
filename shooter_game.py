from pygame import * 
from random import randint 
from time import time as timer
 
mixer.init() 
mixer.music.load('space.ogg') 
mixer.music.play() 
mixer.music.set_volume(0.01) 
fire_sound = mixer.Sound('fire.ogg') 
fire_sound.set_volume(0.01) 
 
lost = 0 
score = 0 
max_lost = 10
goal = 20
life = 3
 
img_back = 'galaxy.jpg' 
img_hero = 'rocket.png' 
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'
 
font.init() 
font2 = font.Font(None, 36) 
win = font2.render('YOU WIN !!!', True, (25, 250, 52)) 
lose = font2.render('YOU LOSE !!!', True, (250, 25, 52))   
 
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image),(size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
 
    def reset(self): 
        window.blit(self.image,(self.rect.x,self.rect.y))  
 
 
class Player(GameSprite): 
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_a] and self.rect.x > 5: 
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < win_width - 80: 
            self.rect.x += self.speed 
     
 
    def fire(self): 
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15) 
        bullets.add(bullet) 
        fire_sound.play() 
 
class Enemy(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost 
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width-80) 
            self.rect.y = 0 
            lost += 1 
 
class Bullet(GameSprite): 
    def update(self): 
        self.rect.y -= self.speed 
        if self.rect.y < 0: 
            self.kill() 
 
win_width = 700 
win_height = 500 
display.set_caption(' Cyberpunk 30234') 
window = display.set_mode((win_width, win_height)) 
background = transform.scale(image.load(img_back), (win_width, win_height)) 
 
ship = Player(img_hero, 5, win_height-100, 80, 100, 10) 
 
bullets = sprite.Group() 
monsters = sprite.Group() 
asteroids = sprite.Group()

for i in range(1, 6): 
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 6)) 
    monsters.add(monster) 

for i in range(1, 3): 
    asteroid = Enemy(img_asteroid, randint(80, win_width-80), -40, 80, 50, randint(1, 3)) 
    asteroids.add(asteroid) 
 
finish = False 
run = True 

num_fire = 0
rel_time = False
last_time = 0

while run: 
    for e in event.get(): 
        if e.type == QUIT: 
            run = False 
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: 
                if num_fire < 5 and not rel_time:
                    ship.fire()
                num_fire += 1

            if num_fire >= 5 and not rel_time:
                last_time = timer()
                rel_time = True
     
    if not finish: 
        window.blit(background, (0, 0)) 
 
        text = font2.render('Счет: ' +str(score), 1, (255, 255, 255)) 
        window.blit(text, (10, 20)) 
 
         
        text_lose = font2.render('Пропущено: ' +str(lost), 1, (255, 255, 255)) 
        window.blit(text_lose, (10, 50)) 
 
        ship.update() 
        ship.reset() 
        monsters.update() 
        monsters.draw(window) 
        bullets.update() 
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                rel = font2.render('Wait, reload. . .', 1, (150, 0, 0))
                window.blit(rel, (260, 460))
            else:
                num_fire = 0
                rel_time = False
 
        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for collide in collides: 
            score += 1 
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster) 
 
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, False)
            sprite.spritecollide(ship, asteroids, False)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
             
        if score >= goal: 
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font2.render("Жизни: " + str(life), 1, life_color)
        window.blit(text_life, (570, 20))
 
        display.update() 
    time.delay(50)

