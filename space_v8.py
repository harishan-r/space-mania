#imports all the needed functions
import pygame, sys, math
from pygame.locals import *
import random


program=True
#highscore outside of loop to remember the highest score
highscore=0
#Loops the entire program
while program:
    #initializes the mixer and pygame
    pygame.mixer.init()   
    pygame.init()
    #The setup of the screen for the game
    size=(1024, 768)
    fpsClock = pygame.time.Clock()
    screen= pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()
    w=screen.get_width()
    h=screen.get_height()
    pygame.display.set_caption ('Space Mania')
    #variables for any colours I use
    white= (pygame.Color(255,255,255))
    blue = (pygame.Color(0,0,255))
    red = (pygame.Color(255, 0, 0))
    #background music
    pygame.mixer.music.load("spacemusic.mp3")
    pygame.mixer.music.play(-1)
    
    #Load all the music, sounds and pictures
    transform=pygame.transform.scale
    rocket=transform(pygame.image.load('rocket_big.png'), (150,150))
    rocket2=transform(pygame.image.load('rocket_big copy.png'), (150,150))
    p1=transform(pygame.image.load('player1_big.png'), (86,20))
    p2=transform(pygame.image.load('player2_big.png'), (86,20))
    space=transform(pygame.image.load('space_big.jpg'), (w,h))
    space2=transform(pygame.image.load('space_big.jpg'), (w,h))
    alien=transform(pygame.image.load('alien_big.png'), (90,57))
    explosion=transform(pygame.image.load('explosion_big.png'), (90,90))
    gameover=transform(pygame.image.load('gameover_big.png'), (350,230))
    big_explosion=transform(pygame.image.load('explosion_big.png'), (300,300))
    boss=transform(pygame.image.load('mediumenemy_big.png'), (200,101))
    playagain=pygame.image.load('playagain.png')
    life=pygame.image.load('lives.png')
    title=pygame.image.load('spacemania_2.jpg')
    highlight=pygame.image.load('highlight.png')
    control_settings=pygame.image.load('controls.jpg')
    laser_sound=pygame.mixer.Sound("laser.wav")
    explosion_sound=pygame.mixer.Sound("explosion.wav")
     
    
    #two different font sizes
    myfont = pygame.font.SysFont("monospace", 24)
    myfont2 = pygame.font.SysFont("monospace", 30)
    
    #scores for each player
    p1_score=0
    p2_score=0
    
    
    #functions used
    def backgrounds():
        '''backgrounds - blitting a background that scrolls downwards'''
        screen.blit(space, (0,background))
        screen.blit(space2,(0,-h+background2))    
    
    def player1(x_movement):
        '''player1(x_movement) - takes in the parameter (x_movement) to control player 1's movement'''
        if active_bullets==True or active_bullets_cooldown%5:
            screen.blit(rocket,(start_x+x_movement-33,start_y))
        screen.blit(p1, (start_x+x_movement,start_y-20))
        
    def player2(x2_movement):
        '''player2(x_movemenet) - takes in the parameter (x2_movment) to control player 2's movement'''
        if active_bullets2==True or active_bullets_cooldown2%5:
            screen.blit(rocket2,(start2_x+x2_movement-33,start_y))
        screen.blit(p2, (start2_x+x2_movement, start_y-20))
    
    def lives(lives_remaining):
        '''lives(lives_remaining) - takes in the parameter (lives_remaining) to print out the number of lives the user has'''
        life_location=w/20
        lives_list=[]
        for x in range(lives_remaining):
            lives_list.append(life_location)
            life_location+=w/20
        for x in lives_list:
            screen.blit(life, (w-x,0))
        
    #starting positions for the players
    start_x=int(w/4)
    start2_x=int(w*3/4)
    start_y=int(h*3/5)
    
    #all the empty variables, list and booleans 
    x2_movement=0
    x_movement=0
    background=0
    background2=0        
    space_counter=0
    l_counter=0
    bullet_y=start_y
    bullets_list=[]
    bullets_list2=[]
    boss_location=[w/2-100,-65]
    boss_timer=0
    boss_hit=0
    boss_explosion=[]
    boss_defeat=0
    explosion_counter=0
    active_bullets=True
    active_bullets2=True
    active_bullets_cooldown=0
    active_bullets_cooldown2=0
    lives_remaining=3
    start_score=0
    enemy_speed=6
    cursor=0
    lasers=[]
    left_boss=False
    right_boss=True
    
    #controls the main loops for the program
    game=False
    victory=False
    ending=False
    main_screen=True
    twoplayer=True
    controls=True
    
    #loop for the home screen
    while main_screen:
        #draws the visuals
        single = myfont2.render("SINGLEPLAYER", 1, (white))
        multi= myfont2.render("MULTIPLAYER", 1, (white))
        controls= myfont2.render("CONTROLS", 1, (white))
        leaderboard=myfont2.render("{0}".format(highscore), 1, (white))
        screen.blit(title, (0,0))    
        screen.blit(highlight, (w/2-w*0.178, h*(0.425+cursor)))
        screen.blit(single, (w/2-w*0.11, h*0.45))
        screen.blit(multi, (w/2-w*0.1, h*0.6))
        screen.blit(controls, (w/2-w*0.075, h*0.75))
        screen.blit(leaderboard, (w*0.8, h*0.08))
        
        #joystick controls
        joystick_count=pygame.joystick.get_count()
        #allows for two players
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYUP:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            #moves the cursor in main screen
            if round(joystick.get_axis(1)) == -1:
                if cursor>0:
                    cursor-=0.1525
            if round(joystick.get_axis(1)) == 1:
                if cursor<0.305:
                    cursor+=0.1525
            #exits the program if button 2 is clicked
            if joystick.get_button(2):
                program=False
                main_screen=False
                sys.exit()
            #selects one of the options (singleplayer, multiplayer or controls)
            if joystick.get_button(1):
                if cursor==0:
                    game=True
                    victory=False
                    ending=True
                    main_screen=False
                    twoplayer=False
                    start_x=int(w/2)
                    enemy_speed-=2
                if cursor==0.1525:
                    game=True
                    victory=False
                    ending=True
                    main_screen=False
                if cursor==0.305:
                    #prints the control screen
                    while True:
                        screen.blit(control_settings, (0,0))
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                        if joystick.get_button(3):
                            break
                        pygame.display.update()
                        fpsClock.tick(30)
        
        #keyboard controls 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYUP:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #horizontal movements
                if event.key== pygame.K_s or event.key==pygame.K_DOWN:
                    if cursor<0.30:
                        cursor+=0.1525
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    if cursor>0:
                        cursor-=0.1525
            elif event.type==KEYDOWN:
                if cursor==0.305:
                    if event.key==K_RETURN:
                        #prints the control screen                            
                        while True:
                            p = pygame.key.get_pressed()
                            screen.blit(control_settings, (0,0))
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                            if p[pygame.K_BACKSPACE]:
                                break
                            pygame.display.update()
                            fpsClock.tick(30)
                            
            p = pygame.key.get_pressed()
            #sets the booleans controlling the main loops - starts the game 
            if p[pygame.K_RETURN]:
                if cursor==0:
                    game=True
                    victory=False
                    ending=True
                    main_screen=False
                    twoplayer=False
                    start_x=int(w/2)
                    enemy_speed-=2
                if cursor==0.1525:
                    game=True
                    victory=False
                    ending=True
                    main_screen=False
                
        
        pygame.display.update()
        fpsClock.tick(30)           
    
    #generates the enemies
    enemies=[]
    for i in range(15):
        x_cord_enemies=random.randint(0,w-90)
        y_cord_enemies=random.randint(-h,-57)
        enemies.append([x_cord_enemies,y_cord_enemies])
    
    #game loop
    while game:
        screen.fill(white)
        #variable for when the boss would be introduced
        boss_activation=start_score+10000
        
        #joy stick controls 
        joystick_count=pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()      
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==KEYUP:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                #resets the counter appending the bullet
                if event.type == pygame.JOYBUTTONUP:
                    if event.button==0:
                        space_counter=0
                    elif event.button==1:
                        l_counter=0
            
            #joystick for first player               
            if i==0:
                #horizontal movements
                if round(joystick.get_axis(0)) == -1:
                    if 0<=start_x+x_movement-10<=w:
                        x_movement -= 12
                if round(joystick.get_axis(0)) == 1:
                    if -8<=start_x+x_movement-10<=w-115:
                        x_movement += 12
                #shoot button for player 1    
                if joystick.get_button (0):
                    #restrictions ensuring that the player is only allowed to shoot at a given time
                    if boss_timer==0 or boss_timer>230 and active_bullets==True:
                        bullet = [(start_x+x_movement+42), bullet_y]
                        if space_counter==0:
                            bullets_list.append(bullet)
                            pygame.mixer.Sound.play(laser_sound)
                            space_counter+=1
                    #during the boss introduction or when the player is hit the bullet list is cleared
                    else: 
                        bullets_list.clear()
            #joystick for second player and checks if two player mode is active                          
            elif i==1 and twoplayer: 
                #horizontal movements
                if round(joystick.get_axis(0)) == -1:
                    if 0<=start2_x+x2_movement-10<=w:
                        x2_movement-=12
                        
                if round(joystick.get_axis(0)) == 1:
                    if -10<=start2_x+x2_movement-10<=w-115:
                        x2_movement+=12
                #shoot button for player 2
                if joystick.get_button (1):
                    #restrictions ensuring that the player is only allowed to shoot at a given time
                    if boss_timer==0 or boss_timer>230 and active_bullets2==True:
                        bullet2=[(start2_x+x2_movement+42), bullet_y]
                        if l_counter==0:
                            bullets_list2.append(bullet2)
                            pygame.mixer.Sound.play(laser_sound)
                            l_counter+=1
                    #during the boss introduction or when the player is hit, the bullet list is cleared
                    else: 
                        bullets_list2.clear()
               
        #keyboard controls                      
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYUP:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #when the players' shoot key is released, their associated counter is reset to allow them to shoot once more
                if event.key == pygame.K_SPACE:
                    space_counter=0
                if event.key == pygame.K_l:
                    l_counter=0
            elif event.type==KEYDOWN:
                #shoot key for player 1
                if event.key == pygame.K_SPACE:
                    #restrictions ensuring that the player is only allowed to shoot at a given time
                    if boss_timer==0 or boss_timer>230 and active_bullets==True:
                        bullet = [(start_x+x_movement+42), bullet_y]
                        if space_counter==0:
                            bullets_list.append(bullet)
                            pygame.mixer.Sound.play(laser_sound)
                            space_counter+=1
                    #during the boss introduction or when the player is hit, the bullet list is cleared
                    else: 
                        bullets_list.clear()
                        
                #shoot key for player 2
                if event.key == pygame.K_l:
                    #restrictions ensuring that the player is only allowed to shoot at a given time
                    if boss_timer==0 or boss_timer>230 and active_bullets2==True:
                        bullet2=[(start2_x+x2_movement+42), bullet_y]
                        if l_counter==0:
                            bullets_list2.append(bullet2)
                            pygame.mixer.Sound.play(laser_sound)
                            l_counter+=1
                    #during the boss introduction or when the player is hit, the bullet list is cleared
                    else: 
                        bullets_list2.clear()
        
        #keyboard controls for player 1
        p = pygame.key.get_pressed()
        if p[pygame.K_a]:
            if 0<=start_x+x_movement-10<=w:
                x_movement -= 10
        if p[pygame.K_d]:
            if -8<=start_x+x_movement-10<=w-115:
                x_movement += 10
        
        #moving background
        if background<h:
            background+=3
        else: 
            background=0
        if -h+background2<0:
            background2+=3
        else: 
            background2=0
        backgrounds()
        
        #creates the player 1 score text into an image (top left corner) 
        p1text = myfont.render("P1 Score {0}".format(p1_score), 1, (white))
        screen.blit(p1text, (w*0.01, w*0.03))
        #the image for the text of the boss
        martian=myfont.render("Martian", 1, (white))
        
        #draws the enemies on the screen
        for enemy in enemies:
            #deletes an enemy if it is out of the screen
            if enemy[0]>w or enemy[0]+90<0:
                enemies.pop(enemies.index(enemy))
            #during boss introduction, enemies move to the sides
            if boss_timer>0:
                if enemy[0]>w/2:
                    enemy[0] += 10
                else: 
                    enemy[0]-=10
            #moving the enemies downwards during regular gameplay
            else:
                enemy[1] += enemy_speed
            screen.blit(alien, enemy)
            #regenerates an enemy if it makes it to the bottom of the screen
            if enemy[1]>=h:
                lives_remaining-=1
                x_cord_enemies=random.randint(0,w-90)
                y_cord_enemies=random.randint(-h,-57)
                enemy[0]=x_cord_enemies
                enemy[1]=y_cord_enemies            
        
        #draws the bullets for the first player        
        for bullet in bullets_list:
            #prevents player to shoot during the boss introduction
            if boss_timer==0 or boss_timer>230:
                pygame.draw.circle(screen, red, bullet, 5, 0)
                #moves bullet upwards
                bullet[1]-=10
                #deletes bullet if it leaves the screen
                if bullet[1]<=0 or bullet[0]<0:
                    bullets_list.pop(bullets_list.index(bullet))
                #collision detection between the bullet and the enemy
                for enemy in enemies:
                    if enemy[0]<=bullet[0]<=enemy[0]+90 and enemy[1]<=bullet[1]<=enemy[1]+57:
                        #adds score, regenerates the enemy and gets rid of bullet
                        p1_score+=100
                        x_cord_enemies=random.randint(0,w-90)
                        y_cord_enemies=random.randint(-h,-57)
                        screen.blit(explosion, enemy)
                        enemy[0]=x_cord_enemies
                        enemy[1]=y_cord_enemies
                        bullet[0]=-300
                #collision detection between the bullet and the boss
                if p1_score+p2_score>=boss_activation and boss_location[0]<=bullet[0]<=boss_location[0]+200 and boss_location[1]<=bullet[1]<=boss_location[1]+85:
                    boss_hit+=1
                    bullet[0]=-300
                    p1_score+=25
        
        #fighting the boss     
        if p1_score+p2_score>=boss_activation and w*0.8-boss_hit*w*0.004>=2:     
            boss_timer+=1
            #introduction of the boss
            if boss_timer>100:
                screen.blit(boss, boss_location)
                pygame.draw.rect(screen, red, (w*0.1,h*0.95, w*0.8-boss_hit*w*0.004,w*0.02))
                screen.blit(martian, (w*0.1, h*0.9))
                
                if boss_location[1]<=w*0.1:
                     boss_location[1]+=3
                #boss fights back
                else: 
                    if boss_timer>230:
                        #boss AI - choosing when to shoot
                        shot_options=[10,20,30]
                        shots_random=random.choice(shot_options)
                        if boss_timer%shots_random==0:
                            lasers.append([int(boss_location[0])+100,int(boss_location[1])+100])
                        #boundaries for the boss - changes directions once it hits the side of the screen
                        if boss_location[0]>=w-200:
                            left_boss=True
                            right_boss=False
                        elif boss_location[0]<=0:
                            left_boss=False
                            right_boss=True
                        if left_boss:
                            boss_location[0]-=enemy_speed-2
                        elif right_boss:
                            boss_location[0]+=enemy_speed-2
        
        #detects when the boss is defeated
        if boss_defeat==0 and w*0.8-boss_hit*w*0.004<2:
            p1_score+=10000
            p2_score+=10000
            victory=True
            explosion_x= boss_location[0]-10
            boss_defeat=1
        
        #boss defeat sequence
        if victory:
            boss_timer+=1
            screen.blit(boss, boss_location)
            #creates explosions around the boss
            if explosion_counter<4 and boss_timer%20==0:    
                if explosion_counter<3:
                    boss_explosion.append([explosion_x, boss_location[1]])
                    explosion_x+=130/2  
                explosion_counter+=1
            #creates the smaller explosions
            for explosion_pos in boss_explosion:
                screen.blit(explosion, explosion_pos)
                #prevents players from shooting during defeat sequence
                active_bullets=False
                active_bullets2=False
                #explosion sound effect
                if explosion_counter==3:
                    pygame.mixer.Sound.play(explosion_sound)
                #final large explosion and setup for the next level
                if explosion_counter==4:
                    screen.blit(big_explosion, (boss_location[0]-50, boss_location[1]-100))
                    victory=False
                    boss_timer=0
                    boss_hit=0
                    boss_defeat=0
                    explosion_counter=0
                    enemy_speed+=1
                    boss_location=[w/2-100,-65]
                    boss_explosion.clear()
                    enemies=[]
                    #regenerates the enemies 
                    for i in range(15):
                        x_cord_enemies=random.randint(0,w-90)
                        y_cord_enemies=random.randint(-h,-57)
                        enemies.append([x_cord_enemies,y_cord_enemies])
                        start_score=p1_score+p2_score                                     
        
        #deactivating player 1's bullets   
        if active_bullets==False:
            active_bullets_cooldown+=1
            if active_bullets_cooldown>=75:
                active_bullets=True
                active_bullets_cooldown=0
        
        #drawing the lasers for the boss
        for laser_location in lasers:
            pygame.draw.circle(screen, blue,(laser_location[0], laser_location[1]), 8, 0)
            #moves the laser downwards
            laser_location[1]+=15
            #collision detection between the laser and player 1
            if start_x+x_movement+10<=laser_location[0]<=start_x+x_movement+75 and start_y<=laser_location[1]<=start_y+125 and active_bullets==True:
                lasers.pop(lasers.index(laser_location))
                active_bullets=False
                lives_remaining-=1
            #collision detection between the laser and player 2
            elif twoplayer and start2_x+x2_movement+10<=laser_location[0]<=start2_x+x2_movement+75 and start_y<=laser_location[1]<=start_y+125 and active_bullets2==True:
                lasers.pop(lasers.index(laser_location))
                active_bullets2=False
                lives_remaining-=1
            #deletes the laser if it goes below the page
            if laser_location[1]>h:
                lasers.pop(lasers.index(laser_location))
        
        #detects if the player(s) lost
        if lives_remaining<=0:
            #breaks the game and makes the game over screen True
            game=False
            ending=True
            #adds the highscore
            if p1_score>p2_score and p1_score>highscore:
                highscore=p1_score
            elif p2_score>p1_score and p2_score>highscore:
                highscore=p2_score
            elif p1_score==p2_score and p1_score>highscore:
                highscore=p1_score
        
        #Player 2 Settings - in case of singleplayer this is deactivated   
        if twoplayer:
            #keyboard movements for player 2
            if p[pygame.K_LEFT]:
                if 0<=start2_x+x2_movement-10<=w:
                    x2_movement-=12
            if p[pygame.K_RIGHT]:
                if -10<=start2_x+x2_movement-10<=w-115:
                    x2_movement+=12
            #creates the player 2 score text into an image (top left corner)
            p2text = myfont.render("P2 Score {0}".format(p2_score), 1, (white))
            screen.blit(p2text, (w*0.01, w*0.07))
            #draws the bullets for the first player
            for bullet in bullets_list2:
                #prevents player to shoot during the boss introduction
                if boss_timer==0 or boss_timer>230:
                    pygame.draw.circle(screen, red, bullet, 5, 0)
                    #moves bullet upwards
                    bullet[1]-=10
                    #deletes bullet if it leaves the screen
                    if bullet[1]<=0 or bullet[0]<0:
                        bullets_list2.pop(bullets_list2.index(bullet))
                    #collision detection between the bullet and the enemy
                    for enemy in enemies:
                        if enemy[0]<=bullet[0]<=enemy[0]+90 and enemy[1]<=bullet[1]<=enemy[1]+57:
                            #adds score, regenerates the enemy and gets rid of bullet
                            p2_score+=100
                            x_cord_enemies=random.randint(0,w-90)
                            y_cord_enemies=random.randint(-h,-57)
                            screen.blit(explosion, enemy)
                            enemy[0]=x_cord_enemies
                            enemy[1]=y_cord_enemies
                            bullet[0]=-300
                    #collision detection between the bullet and the boss
                    if p1_score+p2_score>=boss_activation and boss_location[0]<=bullet[0]<=boss_location[0]+200 and boss_location[1]<=bullet[1]<=boss_location[1]+85:
                        boss_hit+=1
                        bullet[0]=-300
                        p2_score+=25
            
            #deactivating player 2's bullets
            if active_bullets2==False:
                active_bullets_cooldown2+=1
                if active_bullets_cooldown2>=75:
                    active_bullets2=True
                    active_bullets_cooldown2=0
        
        #draws the players                   
        player1(x_movement)
        if twoplayer:
            player2(x2_movement)
        lives(lives_remaining) 
            
        pygame.display.update()
        fpsClock.tick(30)
    
    #setup for blinking GAMEOVER       
    blink_on=0
    blink_off=0
    #setup for 'yes' and 'no' options
    yes=myfont2.render("YES", 1, (white))
    no=myfont2.render("NO", 1, (white))
    #counter for the location of the user's cursor
    down=0
    #game over screen
    while ending:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYUP:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #background moving
        if background<h:
            background+=3
        else: 
            background=0
        if -h+background2<0:
            background2+=3
        else: 
            background2=0
        #draws background and players
        backgrounds()
        player1(x_movement)
        if twoplayer:
            player2(x2_movement)
        #makes the game over image blink
        if blink_on<15:
            screen.blit(gameover, (w/2-175,h/15))
            blink_on+=1
            blink_off=0
        else:
            blink_off+=1
            if blink_off==20:
                blink_on=0
        #blits the play again options 
        screen.blit(playagain, (w/2-75, h/2-25))
        screen.blit(yes, (w/2-24,h/2+25))
        screen.blit(no, (w/2-18,h/2+55))
        #blits the cursor beside the options
        pygame.draw.polygon (screen, white, [[w/2-30,h/2+35+down], [w/2-40,h/2+25+down], [w/2-40,h/2+45+down]])
        #joystick controls to move cursor and select an option
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            if round(joystick.get_axis(1)) == -1:
                down=0
            if round(joystick.get_axis(1)) == 1:
                down=35
            
            if joystick.get_button(1):
                if down==0:
                    game=True
                    ending=False
                else:
                    program=False
                    ending=False
                    sys.exit()
        #keyboard controls to move cursor and select an option           
        p = pygame.key.get_pressed()
        if p[pygame.K_DOWN] or p[pygame.K_s]:
            down=35
        elif p[pygame.K_UP] or p[pygame.K_w]:
            down=0
        elif p[pygame.K_RETURN]:
            #play again - yes
            if down==0:                
                game=True
                ending=False
                main_screen=True
            #play again - no    
            else:
                program=False
                ending=False
        pygame.display.flip()
        fpsClock.tick(30)
    
      
          
        