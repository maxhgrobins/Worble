import tkinter as tk
from functools import partial
import random
from datetime import datetime, timezone
import sys
import os

bgcol = "#692e4b"
framecol = "#8497b3"
keycol = "#374566"
keytextcol = "#e8dcd8"
correctcol = "#50785d"
partialcol = "#cfb463"
wrongcol = "#111323"

current_row = 0
current_col = 0
word = ""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def click(btn):
    global current_row
    global current_col

    if current_col < 5:
        box[current_row][current_col]["text"] = btn
        current_col += 1

def wordgen(word_len):
    if word_len == 5:
        return (random.choice(open(resource_path("5_letters.txt")).read().split())).upper()
    else:
        random.seed(word_len)
        word = (random.choice(open(resource_path("5_letters.txt")).read().split())).upper()
        random.seed()
        return word

def newgame(box,btn):
    global current_row
    global current_col
    global word
    
    difficulty = 5

    current_row = 0
    current_col = 0

    word = wordgen(difficulty)
    wordvar.set(word)

    for x in range(6):
        for y in range(5):
            box[x][y].config(text="",font=("Helvetica", 20),bg=keycol, fg=keytextcol)

    for key in btn:
        key.config(bg=keycol, fg =keytextcol, state="normal")

    winframe.place_forget()
    loseframe.place_forget()
    startframe.place_forget()

    win_btn["text"] = "play again"
    lose_btn["text"] = "try again"

def newdaily(box,btn):
    global current_row
    global current_col
    global word

    current_row = 0
    current_col = 0

    current_date = datetime.now(timezone.utc)
    seed = current_date.year + current_date.month + current_date.day
    word = wordgen(seed)
    wordvar.set(word)

    for x in range(6):
        for y in range(5):
            box[x][y].config(text="",font=("Helvetica", 20),bg=keycol, fg=keytextcol)

    for key in btn:
        key.config(bg=keycol, fg =keytextcol, state="normal")

    winframe.place_forget()
    loseframe.place_forget()
    startframe.place_forget()

    win_btn["text"] = "free play"
    lose_btn["text"] = "free play"

def enter(box, btn):
    global current_row
    global current_col
    global word

    guess = ""

    for letter_box in list(box[current_row][y] for y in range(5)):
        letter = letter_box["text"]
        guess += letter
    
    if guess.lower() not in list(open(resource_path("5_letters.txt")).read().split()):
        #popup saying get good
        return

    for y in range(5):
        letter_box = box[current_row][y]
        letter = letter_box["text"] 
        if letter in word:
            if word[y] == letter:
                letter_box.config(bg=correctcol)
                btn[btn_list.index(letter)].config(bg=correctcol)
            else:
                letter_box.config(bg=partialcol)
                if btn[btn_list.index(letter)]["bg"] == keycol:
                    btn[btn_list.index(letter)].config(bg=partialcol)
        else:
            letter_box.config(bg=wrongcol)
            btn[btn_list.index(letter)].config(bg=wrongcol, state="disabled")

    if guess == word:
        win()
        return

    current_row += 1
    current_col = 0

    if current_row == 6:
        lose()

def delete(box):
    global current_row
    global current_col

    if current_col != 0:
        box[current_row][current_col-1]["text"] = ""
        
        current_col -= 1

def win():
    winframe.place(in_=bf, anchor="c", relx=.5, rely=.5)

def lose():
    loseframe.place(in_=bf, anchor="c", relx=.5, rely=.5)


root = tk.Tk()
root['bg'] = bgcol
root.title("worble")
root.iconbitmap(resource_path("worbleA.ico"))

# create a labeled frame for the keypad buttons
# relief='groove' and labelanchor='nw' are default
bf = tk.LabelFrame(root, bg=framecol, bd=3)
bf.pack(padx=15, pady=10)

box = [[0]*5 for _ in range(6)]

for x in range(6):
    for y in range(5):
        box[x][y] = tk.Label(bf,width=4,height=2,borderwidth=2, relief="groove")
        box[x][y].grid(row=x,column=y,pady=5)
        box[x][y].config(text="",font=("Helvetica", 20),bg=keycol,fg=keytextcol)


# create a labeled frame for the keypad buttons
# relief='groove' and labelanchor='nw' are default
lf = tk.LabelFrame(root, bg=framecol, bd=3)
lf.pack(padx=15, pady=10)

# typical calculator button layout
btn_list = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M"]

# create and position all buttons with a for-loop
# r, c used for row, column grid values
r = 8
c = 0
n = 0
cs = 1
# list(range()) needed for Python3
btn = list(range(len(btn_list)))
for label in btn_list:
    # partial takes care of function and argument
    cmd = partial(click, label)
    # create the button
    btn[n] = tk.Button(lf, text=label, width=3, height= 2, command=cmd, bg=keycol, fg=keytextcol, font=("Helvetica"))
    # position the button
    btn[n].grid(row=r, column=c, columnspan = cs, sticky='')
    btn[n].config(state="disabled")
    # increment button index
    n += 1
    # update row/column position
    c += 1
    if c > 9 and r == 8:
        c = 0
        r += 1
        cs=2
    if c > 8 and r == 9:
        c = 1
        r += 1
        cs=2

enter = partial(enter, box, btn)
delete = partial(delete, box)

# create the button
back_btn = tk.Button(lf, text="back", width=5, bg=wrongcol, fg="white", font=("Helvetica"), command=delete)
# position the button
back_btn.grid(row=10, column=0, columnspan = 2, sticky='nsw')

# create the button
enter_btn = tk.Button(lf, text="enter", width=5, bg=correctcol, fg="white", font=("Helvetica"), command=enter)
# position the button
enter_btn.grid(row=10, column=8, columnspan = 2, sticky='nse')


winframe = tk.Frame(bf, bg= correctcol, width=250, height=500,borderwidth=2,relief="raised")
#winframe.place(in_=bf, anchor="c", relx=.5, rely=.5)

wintext = tk.Label(winframe, text="YOU WIN :)", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
wintext.grid(row=0,column=0,padx=20,pady=20,ipadx=5,ipady=5)

# create the button
win_btn = tk.Button(winframe, text="play again", bg=correctcol, fg="white", font=("Helvetica"), command=partial(newgame,box,btn))
# position the button
win_btn.grid(row=1, column=0,padx=20,pady=20)


loseframe = tk.Frame(bf, bg= wrongcol, width=250, height=500,borderwidth=2,relief="raised")
#loseframe.place(in_=bf, anchor="c", relx=.5, rely=.5)

losetext = tk.Label(loseframe, text="you lose :(", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
losetext.grid(row=0,column=0,padx=20,pady=20,ipadx=5,ipady=5)

wordvar = tk.StringVar()

answertext = tk.Label(loseframe, textvariable=wordvar, font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
answertext.grid(row=2,column=0,padx=20,pady=20,ipadx=5,ipady=5)

# create the button
lose_btn = tk.Button(loseframe, text="try again", fg="white", font=("Helvetica"), bg=correctcol, command=partial(newgame,box,btn))
# position the button
lose_btn.grid(row=1,column=0,padx=20,pady=20)


startframe = tk.Frame(bf, bg=bgcol, width=250, height=500,borderwidth=2,relief="raised")
startframe.place(in_=bf, anchor="c", relx=.5, rely=.5)

starttext = tk.Label(startframe, text="worble", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
starttext.grid(row=0,column=0,padx=2,pady=(20,2),ipadx=5,ipady=5)

credstext = tk.Label(startframe, text="created by max\n inspired by 'Wordle' by Josh Wardle @powerlanguish", font="Helvetica 7", fg=keytextcol,bg=bgcol)
credstext.grid(row=1,column=0,padx=20,pady=2)

# create the button
go_btn = tk.Button(startframe, text="free play", fg="white", font=("Helvetica"), bg=correctcol, command=partial(newgame,box,btn))
# position the button
go_btn.grid(row=2,column=0,padx=20,pady=20)

# create the button
daily_btn = tk.Button(startframe, text="daily worble", fg="white", font=("Helvetica"), bg=correctcol, command=partial(newdaily,box,btn))
# position the button
daily_btn.grid(row=3,column=0,padx=20,pady=20)

root.mainloop()