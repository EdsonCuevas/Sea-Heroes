import pygame, sys, random, time, os
from pygame.locals import *
from button import Button
from Menu import MenuTotal
from JSON import Load

def nivelfacil1():
        
        Configuracion,langueje = Load()

        #Start de pygame
        pygame.init()

        #Pantalla
        W,H = 1280,720
        icon = pygame.image.load("img/Fish animation/fish1.png")
        PANTALLA = pygame.display.set_mode((W,H), pygame.RESIZABLE)
        pygame.display.set_caption("Sea Heros")
        pygame.display.set_icon(icon)

        #Fuentes
        font = pygame.font.SysFont('Bauhaus 93', 60)
        font2 = pygame.font.Font('assets/upheavtt.ttf', 40)
        font3 = pygame.font.Font('assets/upheavtt.ttf', 22)

        #Sonidos
        victory_sound = pygame.mixer.Sound("sound/victorysound.mp3")
        death_sound = pygame.mixer.Sound("sound/deathsound.mp3")
        recolection = pygame.mixer.Sound("sound/recolection.mp3")
        death_sound.set_volume(0.25)
        victory_sound.set_volume(0.3)
        
        #Musica de fondo
        pygame.mixer.music.load("sound/level1.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        #Carga las imagenes de subir y bajar volumen
        sonido_arriba = pygame.image.load("sound/img/volume_up.png")
        sonido_abajo = pygame.image.load("sound/img/volume_down.png")
        sonido_mute = pygame.image.load("sound/img/volume_muted.png")
        sonido_max = pygame.image.load("sound/img/volume_max.png")

        #Fondo
        fondo = pygame.image.load("img/bg.jpg").convert()
        VelFondo = 0

        #Colores
        white = (255, 255, 255)
        black = (0, 0, 0)
        green = (91, 208, 0)
        red = (255, 0, 0)

        #Variables Principales
        fps = 100
        clock = pygame.time.Clock()
        swimming = False
        game_over = False
        score = 0
        victory = False
        sound = True

        
        #Carga de imagenes de botones y el icon de objetivo
        bolsa_ico = pygame.image.load("img/icons/bolsa.png")
        botella_ico = pygame.image.load("img/icons/botella.png")
        flecha_up = pygame.image.load("img/keys/arrowup_alternative_paper.png")
        flecha_down = pygame.image.load("img/keys/arrowdown_alternative_paper.png")
        esc_key = pygame.image.load("img/keys/esc_alternative_paper.png")
        r_key = pygame.image.load("img/keys/r_alternative_paper.png")
        q_key = pygame.image.load("img/keys/q_alternative_paper.png")
        click1 = pygame.image.load("img/keys/mouse_L_pressed_paper.png")

        #Frecuencia de aparicion de botella
        frecuencia_bottle = 2500 #milisegundos
        last_bottle = pygame.time.get_ticks() - frecuencia_bottle

        #Frecuencia de aparicion de bolsa
        frecuencia_bag = 3000 #milisegundos
        ultima_bag = pygame.time.get_ticks() - frecuencia_bag

        def draw_text(text, font, text_col, x,y):
            img = font.render(text, True, text_col)
            PANTALLA.blit(img, (x,y))
        
        def get_font(size):
            return pygame.font.Font("assets/font.ttf", size)

        #Defino la clase para reiniciar el juego
        def reset_game():
            bottle_group.empty()
            bag_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(H / 2)
            pygame.mixer.music.rewind()

        #Defino la funcion de pausa
        def pause():
            paused = True
            while paused:
                
                #si el juego esta pausado baja el volumen y muestra la pausa
                pygame.mixer.music.set_volume(0.0)
                draw_text(Configuracion.get(langueje, {}).get("paused"), font2, black, W / 2.3, 320)
                draw_text(Configuracion.get(langueje, {}).get("continue"), font2, black, W / 3.5, 370)

                #evento para poder cerrar el bucle
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        paused = False
                        pygame.quit()
                        exit()
                    #si se vuelve a presionar escape
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            #reanuda el volumen y termina la pausa
                            pygame.mixer.music.unpause()
                            paused = False
                        if event.key == pygame.K_r:
                            nivelfacil1()
                        if event.key == pygame.K_q:
                            MenuTotal()
                        

                pygame.display.update()
        
        #Todas las funciones del pescado
        class Submarine(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.images = []
                self.index = 0
                self.counter = 0
                for num in range (1, 4):
                    img = pygame.image.load(f"img/submarine/submarine{num}.png")
                    self.images.append(img)
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = [x, y]
                self.vel = 0
                self.clicked = False

            #Aqui definimos todas las actualizacion que afectan al pescado
            def update(self):
                #Gravedad del pescado
                if swimming == True:
                    self.vel += 0.5
                    if self.vel > 8:
                        self.vel = 8
                    if self.rect.bottom < 720:
                        self.rect.y += int(self.vel)

                if game_over == False:
                #Salto del pescado
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        self.vel = -10
    
                    if pygame.mouse.get_pressed()[0] == 0:
                        self.clicked = False
                    

                    #Animaciones del pescado
                    self.counter += 1
                    flap_cooldown = 10

                    if self.counter > flap_cooldown:
                        self.counter = 0
                        self.index += 1
                        if self.index >= len(self.images):
                            self.index = 0
                    self.image = self.images[self.index]

                    #Rotacion del pescado
                    self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
                else:
                    self.image = pygame.transform.rotate(self.images[self.index], -180)

        #La clase de la botella
        class Bottle(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("img/coliders/botella.png")
                self.rect = self.image.get_rect()
                self.rect.topleft = [x,y]

            def update(self):
                #Se quedan en su lugar al morir
                if game_over == False:
                    self.rect.x -= 2

        #La clase de la bolsa
        class Bag(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("img/coliders/bolsa.png")
                self.rect = self.image.get_rect()
                self.rect.topleft = [x,y]

            def update(self):
                if game_over == False:
                    self.rect.x -= 2
                def __init__(self, x, y, image):
                    self.image = image
                    self.rect = self.image.get_rect()
                    self.rect.topleft = (x,y)

        class FuelBar():
            def __init__(self, x, y, w, h, max_hp):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.hp = max_hp
                self.max_hp = max_hp

            def draw(self, surface):
                #calculate fuel ratio
                ratio = self.hp / self.max_hp
                pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
                pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

        #Definimos el boton para pasar al siguiente nivel
        def ButtonNextLevel():
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            NEXT = Button(image=(None), pos=(640, 400),
                                    text_input=Configuracion.get(langueje, {}).get("buttonNext"), font=get_font(50), base_color="White", hovering_color="Green")
            NEXT.changeColor(PLAY_MOUSE_POS)
            NEXT.update(PANTALLA)

            #Bucle para cerrar el juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #Evento para detectar el mouse sobre el boton y funcion de este
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if NEXT.checkForInput(PLAY_MOUSE_POS):
                            from Game import nivelfacil1
                            nivelfacil1()

        #Definimos el boton para salir al menu
        def ButtonExit():
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            NEXT = Button(image=(None), pos=(640, 500),
                                    text_input=Configuracion.get(langueje, {}).get("buttonExit"), font=font, base_color="White", hovering_color="Red")
            NEXT.changeColor(PLAY_MOUSE_POS)
            NEXT.update(PANTALLA)

            #Bucle para cerrar el juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #Evento para detectar el mouse sobre el boton y funcion de este
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if NEXT.checkForInput(PLAY_MOUSE_POS):
                            MenuTotal()

        #Definimos el boton para reiniciar todo el nivel 1
        def ButtonReset():
            
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            NEXT = Button(image=(None), pos=(W / 2, 365),
                                    text_input=Configuracion.get(langueje, {}).get("buttonReset"), font=font2, base_color="White", hovering_color="Green")
            NEXT.changeColor(PLAY_MOUSE_POS)
            NEXT.update(PANTALLA)

            #Bucle para cerrar el juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #Evento para detectar el mouse sobre el boton y funcion de este
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if NEXT.checkForInput(PLAY_MOUSE_POS):
                            from Game import nivelfacil1
                            nivelfacil1()

        #Se declaran los objetos como grupos
        submarine_group = pygame.sprite.Group()
        bottle_group = pygame.sprite.Group()
        bag_group = pygame.sprite.Group()

        #Cordenadas donde aparece el pescado
        flappy = Submarine(100, int(H / 2))
        submarine_group.add(flappy)

        #Carga de imagenes de victoria
        images = []
        for i in range(1,5):
            name = "img/victory_screen/victory"+str(i)+".png"
            images.append(pygame.image.load(name))

        fuel_bar = FuelBar(500, 150, 300, 40, 3000)
        fuel_bar.hp = 3000

        #Bucle principal del juego
        running = True
        while running:

            #Tecla pulsada
            keys = pygame.key.get_pressed()

            #Movimiento en bucle del fondo del juego
            x_relativa = VelFondo % fondo.get_rect().width
            PANTALLA.blit(fondo,(x_relativa - fondo.get_rect().width,0))
            if x_relativa < W:
                PANTALLA.blit(fondo,(x_relativa,0))
            #Velocidad del fondo
            VelFondo -= 2
            #Velocidad del juego total
            clock.tick(fps)

            #Muestra todo en pantalla
            submarine_group.draw(PANTALLA)
            submarine_group.update()
            bottle_group.draw(PANTALLA)
            bottle_group.update()
            bag_group.draw(PANTALLA)
            bag_group.update()
            def keys_on_screen():
                draw_text(Configuracion.get(langueje, {}).get("keysControl"), font2, black, 1040, 380)
                PANTALLA.blit(esc_key, (1030, 410))
                draw_text(Configuracion.get(langueje, {}).get("keysPaused"), font3, black, 1100, 446)
                PANTALLA.blit(r_key, (1030, 460))
                draw_text(Configuracion.get(langueje, {}).get("keysReset"), font3, black, 1100, 490)
                PANTALLA.blit(q_key, (1030, 505))
                draw_text(Configuracion.get(langueje, {}).get("keysExit"), font3, black, 1100, 535)
                PANTALLA.blit(flecha_up, (1020, 545))
                draw_text(Configuracion.get(langueje, {}).get("keysUpMusic"), font3, black, 1100, 577)
                PANTALLA.blit(flecha_down, (1010, 580))
                draw_text(Configuracion.get(langueje, {}).get("keysDownMusic"), font3, black, 1100, 620)

            #Si la victoria todavia no esta hecha muestra el score, texto y controles
            if victory == False:
                #Muestra el score
                draw_text(str(score), font, white, W / 2.1, 20)
                draw_text(("/5"), font, white, W / 2, 20)
                #Muestra el objetivo del juego
                draw_text(Configuracion.get(langueje, {}).get("object"), font2, green, 5, 0)
                draw_text(Configuracion.get(langueje, {}).get("recolet"), font2, white, 5, 30)
                PANTALLA.blit(bolsa_ico, (275, 20))
            
            #Cuando empizas el juego empieza muestra instrucciones
            if swimming == False and game_over == False:
                draw_text(Configuracion.get(langueje, {}).get("swimming"), font2, black, W / 3.4, 340)
                PANTALLA.blit(click1, (562, 315))
                #Funcion que muestre las teclas
                keys_on_screen()
            
            #Revisa que el pescado no se salga del agua
            if flappy.rect.top < 200:
                flappy.rect.top = 200
            
            #Revisa la colision del pescado con la botella
            if pygame.sprite.groupcollide(submarine_group, bottle_group, False, False):
                game_over = True
    
            #Revisa la colision del pescado con la bolsa
            hits = pygame.sprite.groupcollide(submarine_group, bag_group, False, True)

            #bucle donde se van sumando los puntos por colisiones
            for hit in hits:
                score += 1
                recolection.play()

            #Defino la funcion de los controles de volumen
            def AudioControl():
                if keys[pygame.K_DOWN] and pygame.mixer_music.get_volume() > 0.0:
                    pygame.mixer.music.set_volume(pygame.mixer_music.get_volume() - 0.01)
                    PANTALLA.blit(sonido_abajo, (1150,25))
                elif keys[pygame.K_DOWN] and pygame.mixer_music.get_volume() == 0.0:
                    PANTALLA.blit(sonido_mute, (1150,25))

                #Sube volumen
                if keys[pygame.K_UP] and pygame.mixer_music.get_volume() < 1.0:
                    pygame.mixer.music.set_volume(pygame.mixer_music.get_volume() + 0.01)
                    PANTALLA.blit(sonido_arriba, (1150,25))
                elif keys[pygame.K_UP] and pygame.mixer_music.get_volume() == 1.0:
                    PANTALLA.blit(sonido_max, (1150,25))

            #Detecta si el jugador gana
            if score == 5 and game_over == False:
                victory = True
                def WinScreen():
                    #Se limpia todos los objetos
                    bottle_group.empty()
                    bag_group.empty()
                    submarine_group.empty()
                    #Muestra la imagen de victoria animada
                    frame = int(time.time()*10) % 4
                    PANTALLA.blit(images[frame], (0, 0))
                    #Muestra el boton de next
                    ButtonNextLevel()
                    #Se detiene la musica
                    pygame.mixer.music.stop()
                    for sound in hits:
                        victory_sound.play()
                WinScreen()

            #Revisa que el pescado toque el suelo
            if flappy.rect.bottom >= 720:
                game_over = True
                swimming = False
            if game_over == True:
                VelFondo = 0
                
                

            #Checa que el juego no llegue a Game Over
            if game_over == False and swimming == True:
                #Generador de botella
                time_now = pygame.time.get_ticks()
                if time_now - last_bottle > frecuencia_bottle:
                    bottle_spawn = random.randint(-100, 200)
                    bottle = Bottle(W, int(H / 2) + bottle_spawn)
                    bottle_group.add(bottle)
                    last_bottle = time_now

            #Checa que el juego no llegue a Game Over
            if game_over == False and swimming == True:
                #Generador de bolsa
                time_now = pygame.time.get_ticks()
                if time_now - ultima_bag > frecuencia_bag:
                    bag_spawn = random.randint(-100, 200)
                    bag = Bag(W, int(H / 2) + bag_spawn)
                    bag_group.add(bag)
                    ultima_bag = time_now

            #Checa que el juego llegue a GameOver y dibuja los botones
            if game_over == True:
                pygame.mixer.music.stop()
                score = 0
                draw_text(Configuracion.get(langueje, {}).get("overReset"), font2, black, W / 3.5, 330)
                draw_text(Configuracion.get(langueje, {}).get("overExit"), font2, black, W / 3.1, 380)
                PANTALLA.blit(r_key, (490, 310))
                PANTALLA.blit(q_key, (535, 360))
            
            if game_over == True and sound == True:
                death_sound.play()
                sound = False

            
            if swimming == True and game_over == False and victory == False:
                fuel_bar.hp -= 1
                if fuel_bar.hp <= 0:
                    death_sound.play()
                    game_over = True
                        

            #Detecta que el juego empiece
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == VIDEORESIZE:
                     PANTALLA = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.MOUSEBUTTONDOWN and swimming == False and game_over == False:
                    swimming = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and game_over == False and swimming == True:
                        PANTALLA.blit(esc_key, (495, 345))
                        keys_on_screen()
                        pause()
                    if event.key == pygame.K_r:
                        nivelfacil1()
                    if event.key == pygame.K_q:
                        MenuTotal()
                        
                        
            AudioControl()
            pygame.display.update()
        
nivelfacil1()
