import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import math

# Create the GUI window
window = tk.Tk()
window.title("Card Game")
window.geometry("600x700")
window.configure(bg="black")


# Define the card suits and ranks
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King",
         "Joker"]

# Define the special cards
special_cards = [('King', 'Hearts'), ('Ten', 'Diamonds'), ('Queen', 'Hearts'), ('Joker', 'Clubs'), ('Joker', 'Hearts'),
                 ('Joker', 'Diamonds'), ('Joker', 'Spades'), ('Seven', 'Clubs'), ('Ace', 'Spades')]

# Define black special cards
black_special_cards = [('Joker', 'Clubs'), ('Joker', 'Spades'), ('Seven', 'Clubs'), ('Ace', 'Spades')]

# Load card images
card_images = {}
for suit in suits:
    for rank in ranks:
        if rank == "Joker":
            if suit == "Spades" or "Clubs":
                filename = "cards/black_joker.png"
            else:
                filename = "cards/red_joker.png"
        else:
            filename = f"cards/{rank}_of_{suit.lower()}.png"
        image = Image.open(filename)
        image = image.resize((75, 105))
        photo = ImageTk.PhotoImage(image)
        card_images[f"{rank} of {suit}"] = photo

# Create the deck of cards
deck = [(rank, suit) for suit in suits for rank in ranks]

# Create a list for drawn cards
drawn_cards = []

# Create a counter for number of cards drawn, blacks and reds points
number_of_cards_drawn = 0
special_cards_drawn = 0
red_cards_drawn = 0
black_cards_drawn = 0
reds = 0
blacks = 0
blacks_in_deck = 0
points_balance = 500
user_bet = 0

# Create bet true or false mechanism
has_bet = False

# Create json file/check if json file already created
file_path = 'data.json'
if os.path.exists(file_path):
    with open('data.json', 'r') as file:
        existing_data = json.load(file)
    deck = existing_data["deck"]
    drawn_cards = existing_data["drawn_cards"]
    number_of_cards_drawn = existing_data["number_of_cards_drawn"]
    special_cards_drawn = existing_data["special_cards_drawn"]
    red_cards_drawn = existing_data["red_cards_drawn"]
    black_cards_drawn = existing_data["black_cards_drawn"]
    reds = existing_data["reds"]
    blacks = existing_data["blacks"]
    special_cards = existing_data["special_cards"]
    blacks_in_deck = existing_data["blacks_in_deck"]

# Create a label to display the drawn card
card_label = tk.Label(window, bg="black")
card_label.pack(pady=20)


# Function to change UI appearance
def change_appearance_red():
    window.configure(bg="red")
    card_label.config(bg="red", fg="white")
    draw_button.config(bg="red", fg="white")
    deck_status.config(bg="red", fg="white")
    card_text_label.config(bg="red", fg="white")
    drawn_cards_status_label.config(bg="red", fg="white")
    bet_button.config(bg="red", fg="white")
    points_balance_label.config(bg="red", fg="white")
    current_bet_label.config(bg="red", fg="white")


def change_appearance_black():
    window.configure(bg="black")
    card_label.config(bg="black", fg="white")
    draw_button.config(bg="black", fg="white")
    deck_status.config(bg="black", fg="white")
    card_text_label.config(bg="black", fg="white")
    drawn_cards_status_label.config(bg="black", fg="white")
    bet_button.config(bg="black", fg="white")
    points_balance_label.config(bg="black", fg="white")
    current_bet_label.config(bg="black", fg="white")


# Function for betting mechanism
def bet():
    global has_bet, entry, points_balance, user_bet
    has_bet = True
    user_bet = entry.get()
    try:
        user_bet = float(user_bet)
        if user_bet > points_balance or user_bet < 0:
            messagebox.showerror("Error", "Please enter a valid bet.")
        else:
            points_balance = points_balance - user_bet
            points_balance_label.config(text=f"Cash: ${points_balance}")
            current_bet_label.config(text=f"Current bet: ${user_bet}")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a number.")


# Create a function to draw a card and update the label
def draw_card():
    global deck, drawn_cards, number_of_cards_drawn, special_cards_drawn, black_cards_drawn, red_cards_drawn,\
        blacks, reds, blacks_in_deck, file_path, black_special_cards, has_bet, points_balance, user_bet

    if len(deck) > 0:
        number_of_cards_drawn += 1
        random.shuffle(deck)
        card = deck.pop()
        drawn_cards.append(card)
        card_image = card_images[f"{card[0]} of {card[1]}"]
        card_label.config(image=card_image)
        card_label.image = card_image

        # Display card in text
        card_text_label.config(text=f"{card[0]} of {card[1]}")

        # Update the drawn cards label
        drawn_cards_status_label.config(text=f"Drawn cards: {number_of_cards_drawn}")

        # Check blacks and reds and update label
        if card[1] == "Hearts" or card[1] == "Diamonds":
            red_cards_drawn += 1
            points_balance = points_balance - 5
            points_balance_label.config(text=f"Cash: ${points_balance}")
        if card == ("King", "Hearts") or card == ("Joker", "Hearts") or card == ("Joker", "Diamonds")\
                or card == ("Queen", "Hearts") or card == ("Ten", "Diamonds"):
            red_cards_drawn -= 1
        if card in special_cards:
            special_cards_drawn += 1
        if card[1] == "Spades" or card[1] == "Clubs":
            black_cards_drawn += 1
        if card == ("Ace", "Spades") or card == ("Joker", "Spades") or card == ("Joker", "Clubs") or card == \
                ("Seven", "Clubs"):
            black_cards_drawn -= 1

        blacks = black_cards_drawn
        reds = red_cards_drawn + (special_cards_drawn * 2)

        # Check for special cards and put red used cards back in deck
        if card in special_cards:
            drawn_cards.remove(card)
            deck.append(card)
            for card in drawn_cards:
                if card[1] == "Hearts" or card[1] == "Diamonds":
                    drawn_cards.remove(card)
                    deck.append(card)

        # Change appearance if red or black
        if card[1] == "Diamonds" or card[1] == "Hearts":
            change_appearance_red()
        else:
            change_appearance_black()

        # Check if bet successful or not
        if has_bet:
            if card[1] == "Clubs" or card[1] == "Spades":
                print("bet won")
                points_balance = points_balance + round((user_bet * math.sqrt(black_cards_drawn)), 2)
                points_balance_label.config(text=f"Cash: ${points_balance}")
            else:
                print("bet lost")
            has_bet = False
            user_bet = 0
            current_bet_label.config(text=f"Current bet: {user_bet}")

        # Check if no black cards left in deck and end game if so
        if os.path.exists(file_path):
            if card[1] == "Clubs" or card[1] == "Spades":
                blacks_in_deck -= 1
            print(card)
            print(blacks_in_deck)
            if card in black_special_cards:
                print("yes")
        else:
            for card in deck:
                if card[1] == "Clubs" or card[1] == "Spades":
                    blacks_in_deck += 1
                if card == ("Ace", "Spades") or card == ("Joker", "Spades") or card == ("Joker", "Clubs")\
                        or card == ("Seven", "Clubs"):
                    blacks_in_deck -= 1

        # Update json and save data
        data = {'deck': deck, 'special_cards': special_cards, 'drawn_cards': drawn_cards,
                'number_of_cards_drawn': number_of_cards_drawn,
                'special_cards_drawn': special_cards_drawn, 'red_cards_drawn': red_cards_drawn,
                'black_cards_drawn': black_cards_drawn, 'reds': reds, 'blacks': blacks,
                'blacks_in_deck': blacks_in_deck}
        with open('data.json', 'w') as filenames:
            json.dump(data, filenames)

             # Game over screen
        if blacks_in_deck <= 0:
            card_text_label.config(text="Game over")
            os.remove(file_path)
            print(blacks_in_deck)
            draw_button.destroy()
            current_bet_label.destroy()
            entry.destroy()
            bet_button.destroy()


# Create a label to display the card in text
card_text_label = tk.Label(window, text="Card game\n"
                                        "rules:\n"
                                        "1. You can draw a card from a standard 52 card deck\n"
                                        "with four jokers. If you land on a special card, either\n"
                                        "a king of hearts, ten of diamonds, queen of hearts,\n"
                                        "seven of clubs, ace of spades or any joker, all red cards\n"
                                        "get shuffled back into the deck.\n"
                                        "2. For every red card drawn you lose $5.\n"
                                        "3. Before drawing each card you can bet any amount on whether\n"
                                        "the next card drawn will be black. The less black cards in\n"
                                        "the deck more your bet will win.\n"
                                        "4. The game finishes when there are no more black cards\n"
                                        "remaining in the deck.",
                                        font=("Comic Sans MS", 12), fg="white", bg="black")
card_text_label.pack(pady=10)


# Create a button to draw a card
draw_button = tk.Button(window, text="Draw Card", command=draw_card, font=("Comic Sans MS", 12), fg="white", bg="black")
draw_button.pack()

# Create a label to display the deck status
deck_status = tk.Label(window, text="", font=("Comic Sans MS", 12), fg="white", bg="black")
deck_status.pack(pady=10)

# Create a label to display the drawn cards status
drawn_cards_status_label = tk.Label(window, text="", font=("Comic Sans MS", 12), fg="white", bg="black")
drawn_cards_status_label.pack(pady=10)

# Create a cash balance label
points_balance_label = tk.Label(window, text=f"Cash: ${points_balance}", font=("Comic Sans MS", 12),
                                fg="white", bg="black")
points_balance_label.pack(pady=5)

# Create label showing current bet
current_bet_label = tk.Label(window, text=f"Current bet: {user_bet}", font=("Comic Sans MS", 12),
                             fg="white", bg="black")
current_bet_label.pack(pady=5)

# Create an entry box for user to type in bet
entry = tk.Entry(window, bg="white")
entry.pack(pady=5)

# Create a button to bet
bet_button = tk.Button(window, text="Bet", command=bet, font=("Comic Sans MS", 12), fg="white", bg="black")
bet_button.pack(pady=5)

# Run the GUI loop
window.mainloop()
