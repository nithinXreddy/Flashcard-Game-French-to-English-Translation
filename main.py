from tkinter import *
import pandas
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"   #insepction
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words to learn.csv")
except FileNotFoundError:
    orginal_data = pandas.read_csv("data/french_words.csv")
    to_learn = orginal_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(card_title, text= "English", fill="white")
    canvas.itemconfig(card_word, text= current_card["English"], fill="white")
    canvas.itemconfig(card_bg, image = card_back_img)


def next_card():
    global current_card, flip_timer
    if not to_learn:
        window.after_cancel(flip_timer)
        canvas.itemconfig(card_title, text="\nEND", font=("Ariel", 100, "bold"), fill="black")
        canvas.itemconfig(card_word, text="", fill="black")
        canvas.itemconfig(card_bg, image=card_front_img)
        return

    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)



def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words to learn.csv", index =False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg = BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image= card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text= "", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text = " ", font=("Ariel", 60, "bold"))
canvas.grid(column= 0, row= 0, columnspan= 2)

cross_image = PhotoImage(file= "images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column= 1)

next_card()



window.mainloop()
