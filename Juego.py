import pygame,time, random, sys

pygame.init()

# Valores iniciales ---------------------------------
Black = (0,0,0)
Coordenada_x = 30
Coordenada_y = 600
Size = (1280,720) 
Fps = 60
Main_Menu = True
GameOver = False
Done = True
Font_score = pygame.font.SysFont('Bodoni MT',25)
Font_score2 = pygame.font.SysFont('Bodoni MT',25)
Score = 0
CounterGameOver = 0
# Parametros de pantalla ----------------------------
Screen  = pygame.display.set_mode(Size)
pygame.display.set_caption("Trabajo Practico")
Clock = pygame.time.Clock()


# Clase del jugador ---------------------------------
class PLayer(pygame.sprite.Sprite):

    # Definicion de variables
    def __init__(self):
       super().__init__()
       self.image = pygame.image.load("Image0.png")   
       self.rect = self.image.get_rect()
       self.ImagesRunRight = []
       self.ImagesRunLeft = []
       self.ImagesIdleRight = []
       self.ImagesIdleLeft = []
       self.IndexRun = 0
       self.IndexIdle = 0
       self.CounterRun = 0
       self.CounterIdle = 0
       self.MovementPlatform = 470
       self.Increment_move = 1
       self.score = 0
       
       for i in range(8,14):
            ImgRight = pygame.image.load(f'Image{i}.png')
            ImgRight = pygame.transform.scale(ImgRight,(50,70))
            ImgLeft = pygame.transform.flip(ImgRight,True,False)
            self.ImagesRunLeft.append(ImgLeft)
            self.ImagesRunRight.append(ImgRight)
       for x in range(0,5):
            ImgIdleRight = pygame.image.load(f'Image{x}.png')
            ImgIdleRight = pygame.transform.scale(ImgIdleRight,(50,70))
            ImgIdleLeft = pygame.transform.flip(ImgIdleRight,True,False)
            self.ImagesIdleRight.append(ImgIdleRight)
            self.ImagesIdleLeft.append(ImgIdleLeft)

       self.rect.x = Coordenada_x
       self.rect.y = Coordenada_y
       self.Velocity_y = 0
       self.IsJumping = False
       self.direction = 0
       self.direction_idle = 1
       self.JumpDelay = 2
       self.CounterJump = 0
       

    # Actualizacion del jugador
    def UpdatePlayer(self):
        AnimationTime = 5
        Increment_x = 0
        Increment_Y = 0
        # Manejo de eventos
        # Movimiento
        Key = pygame.key.get_pressed()
        if Key[pygame.K_d] and GameOver == False:
            self.CounterRun += 1
            self.CounterIdle = 5
            self.direction = 1
            self.direction_idle = 1
            Increment_x +=3
        if Key[pygame.K_a] and GameOver == False:
            self.CounterRun += 1
            self.CounterIdle = 5
            self.direction = -1
            self.direction_idle = -1
            Increment_x -= 3
        if Key[pygame.K_a] == False and Key[pygame.K_d] == False and GameOver == False:
            self.CounterRun = 0
            self.CounterIdle += 0.4
            self.IndexRun = 0
            self.direction = 0


        # Salto del personaje    
            
        self.CounterJump += self.JumpDelay
        if self.CounterJump >55:
            self.CounterJump=55
        if Key[pygame.K_SPACE] and self.IsJumping == False and self.CounterJump >50:
            self.Velocity_y = -15
            self.IsJumping = True
            self.CounterJump = 0
       
        # Agregar gravedad para salto
        self.Velocity_y += 1
        if self.Velocity_y > 10:
            self.Velocity_y = 10
        Increment_Y += self.Velocity_y

        # Animaciones
        if self.CounterRun > AnimationTime:
            self.CounterRun = 0
            self.IndexRun += 1
            if self.IndexRun >= len(self.ImagesRunRight)-1:
                self.IndexRun = 0
            if self.IndexRun >= len(self.ImagesRunLeft)-1:
                self.IndexRun = 0
            if self.direction == 1:    
               self.image = self.ImagesRunRight[self.IndexRun]
            if self.direction == -1:  
               self.image = self.ImagesRunLeft[self.IndexRun]
            if self.rect.right < 5:
                self.rect.right = 5

            if self.rect.right > 1280:
                self.rect.right = 1280



        if self.CounterIdle > AnimationTime :
            self.CounterIdle = 0
            self.IndexIdle += 1
            if self.IndexIdle >= len(self.ImagesIdleRight)-1:
                self.IndexIdle = 0  
            if self.direction == 0 and self.direction_idle == 1:  
                self.image = self.ImagesIdleRight[self.IndexIdle]
            if self.direction == 0 and self.direction_idle == -1:  
               self.image = self.ImagesIdleLeft[self.IndexIdle]
       
        # Actualizar coordenadas
        self.rect.x += Increment_x    
        self.rect.y += Increment_Y  
         

        # Modificar personaje en suelo
        if self.rect.bottom > 695 and self.rect.top > 620:
           self.rect.bottom = 695
           self.IsJumping = False
        if self.rect.bottom < 700 and self.rect.left > 660 and self.rect.top < 580 and self.rect.y > 540:
           self.rect.bottom = 605
           self.IsJumping = False
        if self.rect.bottom < 540 and self.rect.left > 460 and self.rect.left < 660 and self.rect.top < 520  and self.rect.y > 440:
           self.rect.bottom = 515
           self.IsJumping = False
        if self.rect.bottom < 460 and self.rect.left > 220 and self.rect.left < 420 and self.rect.top < 420  and self.rect.y > 360:
           self.rect.bottom = 435
           self.IsJumping = False 
        if self.rect.bottom < 380 and self.rect.left > self.MovementPlatform-20 and self.rect.left < self.MovementPlatform+210 and self.rect.top < 320  and self.rect.y > 280:
           self.rect.bottom = 355
           self.IsJumping = False 
           self.rect.x += self.Increment_move
        if self.rect.bottom < 300 and self.rect.left > 870 and self.rect.left < 1150 and self.rect.top < 320  and self.rect.y > 200:
           self.rect.bottom = 275
           self.IsJumping = False 
        if self.rect.bottom < 240 and self.rect.left > 60 and self.rect.left < 850 and self.rect.top < 220  and self.rect.y > 110:
           self.rect.bottom = 185
           self.IsJumping = False 
        
        Screen.blit(self.image,self.rect)  

    def Platform (self):
        self.MovementPlatform += self.Increment_move
        Screen.blit(Platform5,(self.MovementPlatform,360))
        if self.MovementPlatform > 700 or self.MovementPlatform < 470:
            self.Increment_move *= -1
        

    def DrawMenu(self):
        Screen.blit(Background,(0,0))
        

    def Draw(self):
        Screen.blit(Platform1,(0,700))
        Screen.blit(Platform2,(700,610))
        Screen.blit(Platform3,(500,520))
        Screen.blit(Platform4,(260,440))
        Screen.blit(Platform6,(900,280))
        Screen.blit(Platform7,(100,190))
        
     # Colisiones con monedas e impresion de monedas tomadas
    def AddCoin(self):
        hit = pygame.sprite.spritecollide(pLayer, coin_list, True)
        coin_list.draw(Screen)
        if hit:
            sound1.play()
            self.score += 1  
            
        Text = Font_score.render('Score:  ' + str(self.score), True, Black)
        Screen.blit(Text,(10,10))

        
    
# clase para botones
class Button(): 
    def __init__ (self1,imagebutton,posx, posy):
        self1.imagess = imagebutton
        self1.rect1 = self1.imagess.get_rect()
        self1.posx= posx
        self1.posy= posy
        self1.Iniciate = 0
        self1.Quit = 0
    
    def DrawButtonExit(self1):
       Screen.blit(self1.imagess,(self1.posx,self1.posy))
       pos = pygame.mouse.get_pos()
       if pos[0] > self1.posx and pos[0] < self1.posx + 200 and pos[1] > self1.posy and pos[1] < self1.posy + 45:
           if pygame.mouse.get_pressed()[0] == 1:
               self1.Quit = 1
       
    def DrawButtonStart(self1):
       Screen.blit(self1.imagess,(self1.posx,self1.posy))
       pos1 = pygame.mouse.get_pos()
       if pos1[0] > self1.posx and pos1[0] < self1.posx + 200 and pos1[1] > self1.posy and pos1[1] < self1.posy + 45:
           if pygame.mouse.get_pressed()[0] == 1:
                self1.Iniciate = 1


class Coins (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coins.png")   
        self.rect = self.image.get_rect()

class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load("Enemigo0.png")
        self.rect = self.image1.get_rect()
        self.image2 = pygame.image.load("Enemigo0.png")
        self.rect2 = self.image2.get_rect()
        self.image3 = pygame.image.load("Enemigo0.png")
        self.rect3 = self.image3.get_rect()
        self.ImagesRunRightenemy_1 = []
        self.ImagesRunLefttenemy_1 = []
        self.ImagesRunRightenemy_2 = []
        self.ImagesRunLefttenemy_2 = []
        self.ImagesRunRightenemy_3 = []
        self.ImagesRunLefttenemy_3 = []
        self.increment_1 = 2
        self.increment_2 = 2
        self.increment_3 = 2
        self.movement_1 = 700
        self.movement_2 = 760
        self.movement_3 = 1200
        self.IndexRunEnemy1 = 0
        self.IndexRunEnemy2 = 0
        self.IndexRunEnemy3 = 0
        self.directionenemy1 = 1
        self.directionenemy2 = 1
        self.directionenemy3 = 1
        self.animationenemy = 5
        self.counterenemy1 = 0
        self.counterenemy2 = 0
        self.counterenemy3 = 0

        for h in range(0,5):
            ImgRight1 = pygame.image.load(f'Enemigo{h}.png')
            ImgRight1 = pygame.transform.scale(ImgRight1,(50,70))
            ImgLeft1 = pygame.transform.flip(ImgRight1,True,False)
            self.ImagesRunLefttenemy_1.append(ImgLeft1)
            self.ImagesRunRightenemy_1.append(ImgRight1)
        for l in range(0,5):
            ImgRight2 = pygame.image.load(f'Enemigo{l}.png')
            ImgRight2 = pygame.transform.scale(ImgRight2,(50,70))
            ImgLeft2 = pygame.transform.flip(ImgRight2,True,False)
            self.ImagesRunLefttenemy_2.append(ImgLeft2)
            self.ImagesRunRightenemy_2.append(ImgRight2)
        for r in range(0,5):
            ImgRight3 = pygame.image.load(f'Enemigo{r}.png')
            ImgRight3 = pygame.transform.scale(ImgRight3,(50,70))
            ImgLeft3 = pygame.transform.flip(ImgRight3,True,False)
            self.ImagesRunLefttenemy_3.append(ImgLeft3)
            self.ImagesRunRightenemy_3.append(ImgRight3) 

    def AddEnemy(self):
        self.movement_1 += self.increment_1
        Screen.blit(self.image1,(self.movement_1,550))
        if self.movement_1 < 700 or self.movement_1 > 1220:
            self.increment_1 *= -1
            self.directionenemy1 *= -1

        self.movement_2 += self.increment_2
        Screen.blit(self.image2,(self.movement_2,120))
        if self.movement_2 < 60 or self.movement_2 > 760:
            self.increment_2 *= -1
            self.directionenemy2 *= -1

        self.movement_3 += self.increment_3
        Screen.blit(self.image3,(self.movement_3,638))
        if self.movement_3 < 20 or self.movement_3 > 1220:
            self.increment_3 *= -1
            self.directionenemy3 *= -1

        self.counterenemy1 += 0.8
        self.counterenemy2 += 0.8
        self.counterenemy3 += 0.8

        if self.counterenemy1 > self.animationenemy:
            self.counterenemy1 = 0
            self.IndexRunEnemy1 += 1
            if self.IndexRunEnemy1 >= len(self.ImagesRunRightenemy_1):
                    self.IndexRunEnemy1 = 0
            if self.IndexRunEnemy1 >= len(self.ImagesRunLefttenemy_1):
                    self.IndexRunEnemy1 = 0
            if self.directionenemy1  == 1: 
                self.image1 = self.ImagesRunRightenemy_1[self.IndexRunEnemy1]
            if self.directionenemy1 == -1:  
                self.image1 = self.ImagesRunLefttenemy_1[self.IndexRunEnemy1]

        if self.counterenemy2 > self.animationenemy:
            self.counterenemy2 = 0
            self.IndexRunEnemy2 += 1
            if self.IndexRunEnemy2 >= len(self.ImagesRunRightenemy_2):
                    self.IndexRunEnemy2 = 0
            if self.IndexRunEnemy2 >= len(self.ImagesRunLefttenemy_2):
                    self.IndexRunEnemy2 = 0
            if self.directionenemy2  == 1: 
                self.image2 = self.ImagesRunRightenemy_2[self.IndexRunEnemy2]
            if self.directionenemy2 == -1:  
                self.image2 = self.ImagesRunLefttenemy_2[self.IndexRunEnemy2]

        if self.counterenemy3 > self.animationenemy:
            self.counterenemy3 = 0
            self.IndexRunEnemy3 += 1
            if self.IndexRunEnemy3 >= len(self.ImagesRunRightenemy_3):
                    self.IndexRunEnemy3 = 0
            if self.IndexRunEnemy3 >= len(self.ImagesRunLefttenemy_3):
                    self.IndexRunEnemy3 = 0
            if self.directionenemy3  == 1: 
                self.image3 = self.ImagesRunRightenemy_1[self.IndexRunEnemy3]
            if self.directionenemy3 == -1:  
                self.image3 = self.ImagesRunLefttenemy_3[self.IndexRunEnemy3]
        

coin_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()


for k in range (10):
    coins = Coins()
    coins.rect.x = random.randrange(1000)
    coins.rect.y = random.randrange(500)
    coin_list.add(coins)
    player_list.add(coins)
    
# Busqueda de imagenes
Background = pygame.image.load("Skybackground.png")
Platform1 = pygame.image.load("Mainfloor.png")
Platform2 = pygame.image.load("Ramp.png")
Platform3 = pygame.image.load("Ramp2.png")
Platform4 = pygame.image.load("Ramp2.png")
Platform5 = pygame.image.load("Ramp2.png")
Platform6 = pygame.image.load("Ramp3.png")
Platform7 = pygame.image.load("Ramp4.png")
StartGame = pygame.image.load("Start.png")
Exit = pygame.image.load("Exit.png")


sound1 = pygame.mixer.Sound("Sound.ogg")
sound2 = pygame.mixer.Sound("Sound2 (1).ogg")

pLayer = PLayer()
enemy = Enemy()
buttonstargame = Button(StartGame, 380, 320)
buttonexit = Button(Exit, 680, 320)



# Bucle principal------------------------------------------
while Done:

    if GameOver == True:
        CounterGameOver += 4
        pygame.draw.circle(Screen,Black,(640,360),1000,CounterGameOver)
        # Restaurar valores
        if CounterGameOver > 1000:
            GameOver = False
            Main_Menu = True
            buttonstargame.Iniciate = 0
            buttonexit.Quit = 0
            enemy.increment_1 = 2
            enemy.increment_2 = 2
            enemy.increment_3 = 2
            enemy.movement_1 = 700
            enemy.movement_2 = 760
            enemy.movement_3 = 1200
            enemy.IndexRunEnemy1 = 0
            enemy.IndexRunEnemy2 = 0
            enemy.IndexRunEnemy3 = 0
            enemy.directionenemy1 = 1
            enemy.directionenemy2 = 1
            enemy.directionenemy3 = 1
            enemy.animationenemy = 5
            enemy.counterenemy1 = 0
            enemy.counterenemy2 = 0
            enemy.counterenemy3 = 0
            pLayer.IndexRun = 0
            pLayer.IndexIdle = 0
            pLayer.CounterRun = 0
            pLayer.CounterIdle = 0
            pLayer.MovementPlatform = 470
            pLayer.Increment_move = 1
            pLayer.score = 0
            pLayer.rect.x = Coordenada_x
            pLayer.rect.y = Coordenada_y
            pLayer.Velocity_y = 0
            pLayer.IsJumping = False
            pLayer.direction = 0
            pLayer.direction_idle = 1
            Black = (0,0,0)
            Coordenada_x = 30
            Coordenada_y = 600
            Size = (1280,720) 
            Fps = 60
            Main_Menu = True
            GameOver = False
            Done = True
            Font_score = pygame.font.SysFont('Bodoni MT',25)
            Score = 0
            pLayer.JumpDelay = 1
            pLayer.CounterJump = 0
            CounterGameOver = 0

    if GameOver == False:
        
        if Main_Menu == True: 
            aux=0
            pLayer.DrawMenu()  
            buttonstargame.DrawButtonStart()
            buttonexit.DrawButtonExit()
            if buttonstargame.Iniciate == 1:
                Main_Menu = False
            if buttonexit.Quit == 1:
                Done = False
                
        else:
                # Metodos
                
            pLayer.DrawMenu()  
            pLayer.UpdatePlayer()
            pLayer.Draw()
            pLayer.Platform()
            pLayer.AddCoin()
            enemy.AddEnemy()


            # colisionando con el enemigo
            
            if pLayer.rect.x < enemy.movement_3 +50 and pLayer.rect.y > 600 and pLayer.rect.y < 640:
                if enemy.movement_3 < pLayer.rect.x:
                    print("IsDead")
                    GameOver = True

            if pLayer.rect.x > enemy.movement_3 -50 and pLayer.rect.y > 610 and pLayer.rect.y < 640:
                if enemy.movement_3 > pLayer.rect.x:
                    print("IsDead")
                    GameOver = True

            if pLayer.rect.x < enemy.movement_1 +50 and pLayer.rect.y > 500 and pLayer.rect.y < 543 :
                if enemy.movement_1 < pLayer.rect.x:
                    print("IsDead")
                    GameOver = True

            if pLayer.rect.x > enemy.movement_1 -50 and pLayer.rect.y > 500 and pLayer.rect.y < 543:
                if enemy.movement_1 > pLayer.rect.x:
                    print("IsDead")
                    GameOver = True

            if pLayer.rect.x < enemy.movement_2 +50 and pLayer.rect.y > 100 and pLayer.rect.y < 123 :
                if enemy.movement_2 < pLayer.rect.x:
                    print("IsDead")
                    GameOver = True

            if pLayer.rect.x > enemy.movement_2 -50 and pLayer.rect.y > 100 and pLayer.rect.y < 123:
                if enemy.movement_2 > pLayer.rect.x:
                    print("IsDead")
                    GameOver = True
            


    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Done = False
    

    # Actualizar
    pygame.display.flip()
    Clock.tick(Fps)
    pygame.display.update()

pygame.quit()