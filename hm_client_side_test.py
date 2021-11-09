import socket
import pygame,sys
clock=pygame.time.Clock()
from pygame.locals import *
from threading import Thread

import time
sock = socket.socket ()
sock.settimeout(0.1)
pygame.init()
WINDOW_SCREEN=(900,600)

pygame.display.set_caption("hangmannna")
colour_white=(255,255,255)
colour_gray=(170,170,170)
smallfont = pygame.font.SysFont('Corbel',35)
smallerfont = pygame.font.SysFont('Corbel',25)
font=pygame.font.SysFont(None,100)
notif="this is an X letter word :D, type"
string="-------------"
boo=True
L1=pygame.image.load("lives=0.png")
L2=pygame.image.load("lives=1.png")
L3=pygame.image.load("lives=2.png")
L4=pygame.image.load("lives=3.png")
L5=pygame.image.load("lives=4.png")
L6=pygame.image.load("lives=5.png")
L7=pygame.image.load("lives=6.png")
hangman=pygame.image.load("hangman.png")
pygame.display.set_icon(hangman)
#====================================================================
PORT = 5050
IPv4 = "26.253.46.146"
ADDR = (IPv4, PORT)
FORMAT = 'utf-8'
HEADER = 64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
#=====================================================================
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recieve():
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg = ""
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
    return msg

def load():
    msg = ""
    while msg != "s":
        msg = recieve()
        if msg != "s":
            print(msg)

# def method_w(): #waiting executioner
#     print("Pick a word for the guesser:", end = "")
#     word = input()
#     send(word)
def method_w(): #waiting executioner.
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    word = ""
    running=True
    while running:
        screen.fill((0, 0, 0))
        draw_text("You're the executioner, please type in the word", smallfont, (255, 255, 255), screen, 100, 250)
        draw_text("executing word:", smallfont, (255, 255, 255), screen, 100, 300)
        draw_text("this gonn lag (not a lil)", smallfont, (255, 255, 255), screen, 100,400)
        text_surface = smallfont.render(word, True, colour_gray)
        screen.blit(text_surface, (330, 300))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_KP_ENTER or event.key == K_RETURN:  # press enter to join the game for testing
                    running=False
                    send(word)
                    method_cw()
                if event.key == K_BACKSPACE:
                    word = word[:-1]
                else:
                    word += event.unicode.upper()
        pygame.display.update()
        clock.tick(30)
def method_c():
 global lives,notif,string
 screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
 click=False #click assigned to prevent bugs
 p=""
 lives=6
 u=0
 notif = "this is an X letter word :D, type"
 string = "-------------"
 while True:
        f=150
        screen.fill((0, 0, 0))
        tries(lives)
        #exit button
        #--------------------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(660, 20, 210, 50)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        #--------------------------------------------------------------
        pygame.draw.rect(screen, colour_gray, button)
        draw_text("EXIT", smallfont, (255, 105, 180), screen, 730, 30)
        draw_text(notif, smallfont, colour_gray, screen, 20, 20)
        draw_text("letter guessed:", smallfont, (255, 105, 180), screen, 150, 500)
        for i in list(string):
            draw_text(i, smallfont, colour_white, screen, f, 250)
            f += 30
        click = False
        #click assigned to prevent bugs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                 pygame.quit()
                 sys.exit()
                if event.key == K_BACKSPACE:
                    p= p[:-1]
                else:
                    p+= event.unicode.upper()
                    if len(p)==1:
                        send(p)
                        draw_text(p, smallfont, (255, 105, 180), screen, 680, 500)
                        p=""
                        string= method_us()
                        notif=method_un()
                        lives=method_ul()
                        u+=1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if u>=1 and "-"not in string:
            ask_for_new_game_room_guesser_won()
        elif lives==0:
            ask_for_new_game_room_executioner_won()
        pygame.display.update()
        clock.tick(100)

# def method_c():
#     print(recieve(), end = "")
#     letter = input()
#     while len(letter)>1:
#         letter= input('I said a letter (no whitespace):')
#     send(letter)
def method_cw(): #spectate room
    global lives,notif,string
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    click=False
    lives=6
    running=True
    u=0
    notif = "this is an X letter word :D, type"
    string = "-------------"
    while running:
        if recieve()=="update":
         string = method_us()
         notif = method_un()
         lives = method_ul()
         u+=1
        else: pass

        if u >= 1 and "-" not in string:
            ask_for_new_game_room_guesser_won()
        elif lives == 0:
            ask_for_new_game_room_executioner_won()

        f = 150
        screen.fill((0, 0, 0))
        tries(lives)
        # exit button
        # --------------------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(660, 20, 210, 50)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        # --------------------------------------------------------------
        pygame.draw.rect(screen, colour_gray, button)
        draw_text("EXIT", smallfont, (255, 105, 180), screen, 730, 30)
        draw_text(notif, smallfont, colour_gray, screen, 20, 20)
        draw_text("this is the executioner window", smallfont, (255, 105, 180), screen, 150, 500)
        for i in list(string):
            draw_text(i, smallfont, colour_white, screen, f, 250)
            f += 30
        click = False
        # click assigned to prevent bugs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(1)
def method_p():
    print(recieve())

def method_us():
    string=recieve()
    return string
def method_un():
    notif=recieve()
    return notif
def method_ul():
    lives=recieve()
    return int(lives)
def method_ueval():
    evall=recieve()
    return evall
def game_init():
    load()
    while True:
        method = recieve()
        method = "method_"+method+"()"
        try:
         eval(method)
        except:
            break

# ============================================================================================
def tries(lives):
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    cmd="screen.blit(L"+str(lives)+",(600,200))"
    eval(cmd)
def mẫu():
 while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==QUIT:
         pygame.quit()
         sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.update()
    clock.tick(10)
def draw_text(text, font, color, surface, x, y):  # i copied this
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
def waiting_guesser():
 while True:
    screen.fill((0,0,0))
    draw_text("You're the guesser, please wait for a bit...", smallfont, (255, 255, 255), screen, 150, 250)
    for event in pygame.event.get():
        if event.type==QUIT:
         pygame.quit()
         sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.update()
    clock.tick(10)
def waiting_executioner():
  word=""
  while True:
    screen.fill((0,0,0))
    draw_text("You're the executioner, please type in the word", smallfont, (255, 255, 255), screen, 100, 250)
    draw_text("executing word:", smallfont, (255, 255, 255), screen, 100, 300)
    text_surface=smallfont.render(word,True,colour_gray)
    screen.blit(text_surface,(330,300))
    for event in pygame.event.get():
         if event.type==QUIT:
          pygame.quit()
          sys.exit()
         if event.type==KEYDOWN:
             if event.key==K_ESCAPE:
                 pygame.quit()
                 sys.exit()
             if event.key == K_BACKSPACE:
                word = word[:-1]
             else:
                word += event.unicode.upper()
    pygame.display.update()
    clock.tick(10)
def waiting_room():#find a way to direct to other room
  screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
  running=True
  while running:
      screen.fill((0,0,0))
      draw_text("waiting for other player...", font, (255, 255, 255), screen,20, 250)
      for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == KEYDOWN:
              if event.key == K_ESCAPE:
                  running = False
      pygame.display.update()
      clock.tick(1)
def main_menu():
  click=False

  while True:
    screen.fill((0,0,0))
    #guesser: 61,303; guesser_win2: 21,300
    mx,my=pygame.mouse.get_pos()
    button_1=pygame.Rect(320,100,200,50)
    button_2 = pygame.Rect(320, 170, 200, 50)
    if button_1.collidepoint((mx,my)):
        if click:
            pass
    if button_2.collidepoint((mx,my)):
        if click:
            pygame.quit()
            sys.exit()
    pygame.draw.rect(screen, colour_gray, button_1)
    pygame.draw.rect(screen, colour_gray, button_2)
    draw_text("hang man", font, (255,255,255), screen,250,20)
    draw_text("PLAY",smallfont, (255,105,180), screen,380,110)
    draw_text("QUIT",smallfont, (255,105,180), screen,380,180)
    draw_text("click then wait for a bit..", smallerfont, (255, 105, 180), screen, 550, 110)
    click = False
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            if event.button==1:
               click=True
    pygame.display.update()
    clock.tick(1)
def play(): #plan: update--> shows
    global notif,string
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    click=False #click assigned to prevent bugs
    update=False
    lives=6
    while True:
        if update==True:
            string, notif, lives=method_u()
            update=False
        f=150
        screen.fill((0, 0, 0))
        draw_text(notif, smallfont, colour_white, screen, 20, 20)
        for i in list(string):
         draw_text(i,smallfont,colour_gray,screen,f,250)
         f+=20
        tries(lives)
        #exit button
        #--------------------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(660, 20, 210, 50)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        #--------------------------------------------------------------
        pygame.draw.rect(screen, colour_gray, button)
        draw_text("EXIT", smallfont, (255, 105, 180), screen, 730, 30)
        click = False
        #click assigned to prevent bugs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               update=True
               if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(50)
def ask_for_new_game_room_guesser_won():
    global lives,notif,string
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    click = False
    running = True
    add=""
    k=0
    g=0
    sent=False
    while running:
        f = 150
        screen.fill((0, 0, 0))
        # exit button
        # --------------------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(660, 20, 210, 50)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        # --------------------------------------------------------------
        pygame.draw.rect(screen, colour_gray, button)
        draw_text("EXIT", smallfont, (255, 105, 180), screen, 730, 30)
        draw_text(notif, smallfont, colour_gray, screen, 20, 20)
        draw_text("guesser won and i dont care", smallfont, colour_gray, screen, 150, 400)
        draw_text("another game?(Y/N)", smallfont, colour_white, screen, 150, 500)
        text_surface = smallfont.render(add, True, colour_gray)
        screen.blit(text_surface, (450, 500))
        for i in list(string):
            draw_text(i, smallfont, colour_white, screen, f, 250)
            f += 30
        click = False
        if sent==True:
            draw_text("Confirm? (Y/N)", smallfont, colour_white, screen, 150, 550)
            if k==2:
               if recieve()=="cont":
                g+=1
                if recieve() == "cont" and g==1:
                 running=False
                 pygame.display.quit()
                 game_init()
        # click assigned to prevent bugs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_BACKSPACE:
                    add = add[:-1]
                else:
                    add += event.unicode.upper()
                    if len(add) == 1:
                        send(add)
                        add = ""
                        sent = True
                        k += 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(10)
def ask_for_new_game_room_executioner_won():
    global lives, notif, string
    screen = pygame.display.set_mode(WINDOW_SCREEN, 0, 32)
    click = False
    running = True
    add=""
    sent=False
    k=0
    g=0
    while running:
        f = 150
        screen.fill((0, 0, 0))
        # exit button
        # --------------------------------------------------------------
        mx, my = pygame.mouse.get_pos()
        button = pygame.Rect(660, 20, 210, 50)
        if button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        # --------------------------------------------------------------
        pygame.draw.rect(screen, colour_gray, button)
        draw_text("EXIT", smallfont, (255, 105, 180), screen, 730, 30)
        draw_text(notif, smallfont, colour_gray, screen, 20, 20)
        draw_text("executioner won and i care", smallfont, colour_gray, screen, 150, 400)
        draw_text("another game?(Y/N)", smallfont, colour_white, screen, 150, 500)
        text_surface = smallfont.render(add, True, colour_gray)
        screen.blit(text_surface, (450, 500))

        for i in list(string):
            draw_text(i, smallfont, colour_white, screen, f, 250)
            f += 30
        click = False
        if sent==True:
            draw_text("Confirm? (Y/N)", smallfont, colour_white, screen, 150, 550)
            if k==2:
               if recieve()=="cont":
                g+=1
                if recieve() == "cont" and g==1:
                 running=False
                 pygame.display.quit()
                 game_init()


        # click assigned to prevent bugs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_BACKSPACE:
                    add = add[:-1]
                else:
                    add += event.unicode.upper()
                    if len(add)==1:
                        send(add)
                        add=""
                        sent=True
                        k+=1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(10)
game_init()
