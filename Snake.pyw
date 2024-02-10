from tkinter import *
import random

Game_width = 500
Game_height = 480
speed = 1000000000

space_size = 35
body_parts = 2
snake_color = '#FFFFFF'
food_color = '#FFFF00'
background_color = '#41980a'

def game_win():
    global speed
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('comic sans', 40), text = "YOU WIN!", fill = 'red')
    restart_button.place(x=0, y = 0)
    main_menub.place(x = 395, y = 0)
    speed = 1000000000
    restart_button.place_forget()
    main_menub.place(x=0,y=0)
        
def menu():
    canvas.pack_forget()
    restart_button.place_forget()
    main_menub.place_forget()
    labelScore.pack_forget()
    user_screen.pack()
    intro.pack()
    easyb.place(relx = 0.5, rely = 0.2, anchor = CENTER)
    mediumb.place(relx = 0.5, rely = 0.3, anchor = CENTER)
    hardb.place(relx = 0.5, rely = 0.4, anchor = CENTER)
    quitb.place(relx = 0.5, rely = 0.5, anchor = CENTER)

def game_quit():
    window.destroy()

def game_start(mode): 
    global snake, food, score, direction,speed
    if mode == 1:
         speed = 90
    elif mode == 2:
         speed = 85
    elif mode == 3:
         speed = 50
    else:
         speed = 100
    
    
    labelScore.pack()
    canvas.pack()
    user_screen.pack_forget()
    intro.pack_forget()
    easyb.place_forget()
    mediumb.place_forget()
    hardb.place_forget()
    quitb.place_forget()
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    
    
    direction = 'down'
    labelScore.config(text="Score:{}".format(score))
    nextTurn(snake, food)
    window.after(speed)

class Snake:
    def __init__(self):
        self.body_parts = body_parts
        self.coordinates = []
        self.ovals = []
        
        for i in range(0, body_parts):
            self.coordinates.append([0,0])
            
        for x,y in self.coordinates:
            ovals = canvas.create_oval(x, y, x+space_size, y+space_size, fill = snake_color, tag = 'snake') 
            self.ovals.append(ovals)

class Food:
    def __init__(self):
        x = random.randint(0, (Game_width//space_size)-1)*space_size
        y = random.randint(0, (Game_height//space_size)-1)*space_size
        
        self.coordinates = [x,y]
        canvas.create_oval(x, y, x + space_size, y + space_size, fill = food_color, tag = 'food')
    
def nextTurn(snake, food):
    global speed

    x,y = snake.coordinates[0]
    
    if direction == 'up':
        y -= space_size
    elif direction == 'down':
        y += space_size
    elif direction == 'left':
        x -= space_size
    elif direction == 'right':
        x += space_size
     
    snake.coordinates.insert(0, (x,y))
    
    ovals = canvas.create_oval(x,y, x+space_size, y+space_size, fill = snake_color, tag = 'food')
    
    snake.ovals.insert(0 , ovals )   
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        
        score += 1
        
        labelScore.config(text = 'Score : {}'.format(score))
        
        canvas.delete('food')
        
        food = Food()
        
        
         
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.ovals[-1])
        del snake.ovals[-1]
        
    if checkCollisions(snake):
        gameOver()  
    else:      
     window.after(speed, nextTurn, snake, food)
    if score >=10:
     game_win() 
        
def changeDirection(new_direction):
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
            
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction 
            
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction 
            
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction         
            
def checkCollisions(snake):
    
    x,y = snake.coordinates[0]
    
    if x<0 or x>Game_width:
        
        return True
    
    elif y<0 or y>Game_height:
        
        return True
    
    for body_part in snake.coordinates[1:]:
        if x== body_part[0] and y == body_part[1]:
            
            return True
    return False    
    
def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ('comic sans', 40), text = "GAME OVER >:D", fill = 'red')
    restart_button.place(x=0, y = 0, )
    main_menub.place(x = 360, y = 0)
     
def restart():
    global snake, food, score, direction, speed
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    labelScore.config(text="Score:{}".format(score))
    nextTurn(snake, food)
    restart_button.place_forget()
    main_menub.place_forget()

window = Tk()
window.title("Snake in The Garden ;)")
window.geometry('500x500')
window.resizable(False, False)

window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))

restart_button = Button(window, text="RESTART", command= restart, font=('comic sans', 20),bg = 'red', width = 8)
restart_button.place_forget()

main_menub = Button(window, text="MENU", command= menu, font=('comic sans', 20),bg = 'yellow',width = 8)
main_menub.place_forget()

score = 0
direction = 'down'

labelScore = Label(window, text ="Score : {}".format(score), font = ('comic sans', 40))
labelScore.pack_forget()

canvas = Canvas(window, bg = background_color, width = Game_width, height = Game_height)
canvas.pack_forget()

user_screen = Frame()
user_screen.pack()

intro = Label(user_screen, text = "Choose a Difficulty", fg = 'black', font = ('comic sans', 40) )
intro.pack()


easyb = Button( text = "EASY MODE 👶", bg = 'green', width = 14, command= lambda: game_start(1))
mediumb = Button( text = 'MEDIUM MODE 🧔', bg = 'yellow', width = 14,command= lambda: game_start(2))
hardb = Button ( text = 'HARD MODE 💀', bg = 'orange', width = 14,command= lambda: game_start(3))
quitb = Button( text = 'QUIT', bg = 'red', width = 14,command= game_quit)

easyb.place(relx = 0.5, rely = 0.2, anchor = CENTER)
mediumb.place(relx = 0.5, rely = 0.3, anchor = CENTER)
hardb.place(relx = 0.5, rely = 0.4, anchor = CENTER)
quitb.place(relx = 0.5, rely = 0.5, anchor = CENTER)

snake = Snake()
food = Food()

nextTurn(snake, food)

window.update()
window.mainloop()