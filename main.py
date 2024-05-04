from tkinter import *
import pandas as pd
import random
BG_COLOR = "#B1DDC6"
FONT = "Arial"
rand_word = {}
dictionary_to_learn = {}


# ---------------- Extracting Data ---------------
try:
    data = pd.read_csv("data/words_yet_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    dictionary_to_learn = original_data.to_dict(orient="records")
else:
    dictionary_to_learn = data.to_dict(orient="records")


def generate_word():
    global rand_word, time_to_change
    window.after_cancel(time_to_change)
    rand_word = random.choice(dictionary_to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(meaning, text=rand_word["French"], fill="black")
    canvas.itemconfig(default_image, image=front_img)
    time_to_change = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(default_image, image=back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(meaning, text=rand_word["English"], fill="white")


# ---------------- Saving Unknown Data ---------------
def save_unknown():
    dictionary_to_learn.remove(rand_word)
    generate_word()
    df = pd.DataFrame(dictionary_to_learn)
    df.to_csv("data/words_yet_learn.csv", index=False)


# ---------------- UI Design ---------------
window = Tk()
window.title("FlashCard Game...")
window.config(padx=50, pady=50, bg=BG_COLOR)
time_to_change = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
default_image = canvas.create_image(400, 263, image=front_img)
canvas.config(bg=BG_COLOR)
title = canvas.create_text(400, 150, text="", font=(FONT, 40, "italic"))
meaning = canvas.create_text(400, 260, text="", font=(FONT, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, command=save_unknown)
right_btn.grid(column=1, row=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=save_unknown)
wrong_btn.grid(column=0, row=1)

generate_word()
window.mainloop()
