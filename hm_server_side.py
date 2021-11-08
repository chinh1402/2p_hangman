import socket
from random import choice
    
PORT = 5050
IPv4 = socket.gethostbyname(socket.gethostname())
ADDR = (IPv4, PORT) #address
FORMAT = 'utf-8'
lives = 4    
HEADER = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def display_hangman(tries):
    stages = [ 
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
          
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,

                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
           
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
 
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
   
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
       
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]
    

def send(p, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    p.send(send_length)
    p.send(message)
    
def recieve(p):
    msg_length = p.recv(HEADER).decode(FORMAT)
    msg = ""
    if msg_length:
        msg_length = int(msg_length)
        msg = p.recv(msg_length).decode(FORMAT)
    return msg

def execute(string, guesses): #can be replace with word if not mistaken (damn u)
    string2 =''
    for i in string: #looping thruu ans
        if i in guesses: #if letter in ans in guesses
            string2+= i
        else:            #if not
            string2+= '-'
    return string2
    
def guessed(string, guess): #string can be replaced as word if not mistaken
    if guess in list(string): #right guess
        return True, string.count(guess)
    global lives
    lives -=1
    return False, 0 #wrong guess
    
def get_role(p1, p2):   
    if choice([0, 1]) ==1:
        return p1, p2
    return p2, p1
    
    
def take_word(p):
    send(p, "w")
    word = recieve(p)
    return word
    
def make_guess(p):
    guess = recieve(p)
    print(guess)
    return guess
    
def print_hangman(p1, p2, lives):
    send(p1, 'p')
    send(p2, 'p')
    send(p1, display_hangman(lives))
    send(p2, display_hangman(lives))
    
def notif(p1, p2, guess, string, appearance):
    send(p1,'p')
    send(p2,'p')
    msg = 'The guesser guessed the letter '+guess+', there is '+str(appearance)+" "+guess
    send(p1,msg)
    send(p2,msg)
    send(p1,'p')
    send(p2,'p')
    msg = 'The string now is: '+string
    send(p1,msg)
    send(p2,msg)

def update_string(p1,p2,string):
    send(p1,string)
    send(p2,string)
def update_notif(p1,p2,guess,appearance):
    msg = 'The guesser guessed the letter '+guess+', there is '+str(appearance)+" "+guess
    send(p1,msg)
    send(p2,msg)
def update_lives(p1,p2,lives):
    send(p1,str(lives))
    send(p2,str(lives))
def update_eval(p):
    send(p,  "update")
def won(winner, p1, p2):
    send(p1,'p')
    send(p2,'p')
    msg = 'The '+winner+' won'
    send(p1,msg)
    send(p2,msg)
    
def ask_for_new_game(p1, p2):
    ans1 = recieve(p1)
    ans2 = recieve(p2)
    if ans1 == 'Y' and ans2 == 'Y':
        print("i wass in here")
        return True
    return False


def start_game(executioner, guesser):
    send(executioner,'p')
    send(executioner,'You are the executioner')
    send(guesser,'p')
    send(guesser,'You are the guesser')
    word = take_word(executioner) #ans
    string = "" #current string
    guesses = [] #guesses which were made
    send(guesser,"c")
    while (string != word) and (lives>0):
        guess = make_guess(guesser) #taking char from guesser #worked
        guesses.append(guess) #appending to guesses (up there) #worked
        right, appearance = guessed(word, guess) #giving key_word in and guessing char in there; returning 1 boolean and 1 int #worked
        string = execute(word, guesses) #looping thruu the string using maths and return the new string (key) #worked
        update_eval(executioner)
        update_string(executioner,guesser, string)
        update_notif(executioner,guesser,guess,appearance)
        update_lives(executioner,guesser,lives)
    if recieve(executioner)==recieve(guesser)=="ok":
        ask_for_new_game(executioner,guesser)

def game_room(p1, p2):
    PLAYING = True
    global lives
    while PLAYING:
        lives = 6
        print("im in gameroom")
        executioner, guesser = get_role(p1, p2)
        start_game(executioner, guesser)
        PLAYING = ask_for_new_game(p1, p2)

def init_game():
    server.listen()
    print("SERVER IS LISTENING ON", IPv4)
    conn1, add1 = server.accept()
    print(add1,"connected")
    send(conn1, "Connected. Waiting for the other player")
    conn2, add2 = server.accept()
    print(add2,"connected")
    send(conn1, "Another player connected. Game will now start")
    send(conn2, "Connected. Game will now start.")
    send(conn1, "s")
    send(conn2, "s")
    game_room(conn1, conn2)

    

init_game()
server.close()
 


    
