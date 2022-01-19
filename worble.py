from cgitb import reset
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

def reset_board(box,btn):
    global current_row
    global current_col

    current_row = 0
    current_col = 0

    for x in range(6):
        for y in range(5):
            box[x][y].config(text="",font=("Helvetica", 20),bg=keycol, fg=keytextcol)

    for key in btn:
        key.config(bg=keycol, fg =keytextcol, state="normal")

    enter_btn.config(state="normal")
    back_btn.config(state="normal")

    hide_frame(winframe)
    hide_frame(loseframe)
    hide_frame(startframe)

def newgame(box,btn):
    global word
    
    difficulty = 5

    word = wordgen(difficulty)
    wordvar.set(word)

    reset_board(box,btn)

    win_btn["text"] = "play again"
    lose_btn["text"] = "try again"

def newdaily(box,btn):
    global word

    current_date = datetime.now(timezone.utc)
    seed = current_date.year + current_date.month + current_date.day
    word = wordgen(seed)
    wordvar.set(word)

    reset_board(box,btn)

    win_btn["text"] = "free play"
    lose_btn["text"] = "free play"

def hide_frame(widget):
    widget.place_forget()

def show_frame(widget):
    widget.place(in_=bf, anchor="c", relx=.5, rely=.5)
    helpframe.lift()

def enter(box, btn):
    global current_row
    global current_col
    global word

    guess = ""

    for letter_box in list(box[current_row][y] for y in range(5)):
        letter = letter_box["text"]
        guess += letter
    
    if guess.lower() not in list(open(resource_path("5_letters.txt")).read().split()):
        show_frame(errorframe)
        root.after(2000, hide_frame, errorframe)
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
            btn[btn_list.index(letter)].config(bg=wrongcol)

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
    show_frame(winframe)

def lose():
    show_frame(loseframe)


root = tk.Tk()
root['bg'] = bgcol
root.title("worble")
root.iconbitmap(resource_path("worbleW.ico"))

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

# create and position button
back_btn = tk.Button(lf, text="back", width=5, bg=wrongcol, fg="white", font=("Helvetica"), command=delete)
back_btn.grid(row=10, column=0, columnspan = 2, sticky='nsw')
back_btn.config(state="disabled")

# create and position button
enter_btn = tk.Button(lf, text="enter", width=5, bg=correctcol, fg="white", font=("Helvetica"), command=enter)
enter_btn.grid(row=10, column=8, columnspan = 2, sticky='nse')
enter_btn.config(state="disabled")


# win frame
winframe = tk.Frame(bf, bg= correctcol, width=250, height=500,borderwidth=2,relief="raised")

wintext = tk.Label(winframe, text="YOU WIN :)", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
wintext.grid(row=0,column=0,padx=20,pady=20,ipadx=5,ipady=5)

# create and position button
win_btn = tk.Button(winframe, text="play again", bg=correctcol, fg="white", font=("Helvetica"), command=partial(newgame,box,btn))
win_btn.grid(row=1, column=0,padx=20,pady=20)


# lose frame
loseframe = tk.Frame(bf, bg= wrongcol, width=250, height=500,borderwidth=2,relief="raised")

losetext = tk.Label(loseframe, text="you lose :(", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
losetext.grid(row=0,column=0,padx=20,pady=20,ipadx=5,ipady=5)

wordvar = tk.StringVar()

answertext = tk.Label(loseframe, textvariable=wordvar, font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
answertext.grid(row=2,column=0,padx=20,pady=20,ipadx=5,ipady=5)

# create and position button
lose_btn = tk.Button(loseframe, text="try again", fg="white", font=("Helvetica"), bg=correctcol, command=partial(newgame,box,btn))
lose_btn.grid(row=1,column=0,padx=20,pady=20)


# help frame
helpframe = tk.Frame(bf, bg=bgcol, width=250, height=500,borderwidth=2,relief="raised")

helptext = tk.Label(helpframe, text="""Try and guess the word in 6 tries.
                                        
After entering a guess, the colour of the letters will signal how close you were.

Green   -   correct letter, correct position
Yellow  -   correct letter, incorrect position
Black   -   incorrect letter, incorrect position

Happy worbling!""", font="Helvetica 10", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken",wraplength=280, justify="left")
helptext.grid(row=0,column=0,padx=2,pady=2,ipadx=10,ipady=10)

# create and position button
help_back_btn = tk.Button(helpframe, text="back", fg="white", font=("Helvetica"), bg=correctcol, command=lambda:[show_frame(startframe),hide_frame(helpframe)])
help_back_btn.grid(row=1,column=0,padx=20,pady=20)


# start frame
startframe = tk.Frame(bf, bg=bgcol, width=250, height=500,borderwidth=2,relief="raised")
show_frame(startframe)

starttext = tk.Label(startframe, text="worble", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
starttext.grid(row=0,column=0,padx=2,pady=(20,2),ipadx=5,ipady=5)

credstext = tk.Label(startframe, text="created by max\n inspired by 'Wordle' by Josh Wardle @powerlanguish", font="Helvetica 7", fg=keytextcol,bg=bgcol)
credstext.grid(row=1,column=0,padx=20,pady=2)

# create and position button
go_btn = tk.Button(startframe, text="free play", fg="white", font=("Helvetica"), width = 10, bg=correctcol, command=partial(newgame,box,btn))
go_btn.grid(row=2,column=0,padx=20,pady=20)

# create and position button
daily_btn = tk.Button(startframe, text="daily worble", fg="white", font=("Helvetica"), width = 10, bg=correctcol, command=partial(newdaily,box,btn))
daily_btn.grid(row=3,column=0,padx=20,pady=20)

# create and position button
htp_btn = tk.Button(startframe, text="how to play", fg="white", font=("Helvetica"), width = 10, bg=correctcol, command=lambda:[show_frame(helpframe),hide_frame(startframe)])
htp_btn.grid(row=4,column=0,padx=20,pady=20)


# error frame
errorframe = tk.Frame(bf, bg=bgcol, width=250, height=500,borderwidth=2,relief="raised")

errortext = tk.Label(errorframe, text="not in word list", font="Helvetica 20", fg=keytextcol,bg=keycol,borderwidth=2,relief="sunken")
errortext.grid(row=0,column=0,padx=2,pady=(2),ipadx=5,ipady=5)

root.mainloop()