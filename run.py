import gspread
from google.oauth2.service_account import Credentials
from hangman_art import stages, logo
from hangman_words import word_list
import random
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_user_scores')

gamers = SHEET.worksheet('gamers')
hilltop = SHEET.worksheet('hilltop')

data = gamers.get_all_values()

data2 = hilltop.get_all_values()


# Opening game logo
print(logo)

# Get the high player score and print below game logo


if len(data2) > 1:
    player = hilltop.col_values(1)[1]
    high_score = hilltop.col_values(2)[1]
    print(f"Top Scorer:-{player} Score:{high_score}")
else:
    print("No high scores yet!")

# Function to get or update the number of games played


def get_and_update_games_played(player_name):
    records = gamers.get_all_records()

    # Searching for the player's record
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            new_games_played = record['games_played'] + 1
            gamers.update_cell(idx, 3, new_games_played)
            return new_games_played

    # If player is not found, add them to the sheet with 1 game played and return 1
    gamers.append_row([player_name, None, 1])
    return 1



word_list = word_list
chosen_word = random.choice(word_list)
word_length = len(chosen_word)
player_name = input("What is your name?: ")
games_played = get_and_update_games_played(player_name)
wrong_answers = 0
score = 0


# Function to calculate average score
def average_score(player_name, wrong_answers):

    global games_played
    global score
    records = gamers.get_all_records()
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            total_wrong_answers = (
                int(record.get('total_wrong_answers') or 0) +
                wrong_answers
            )
            
            score = total_wrong_answers / games_played
            print(score)
            print(games_played)

            gamers.update_cell(idx, 4, total_wrong_answers)
            gamers.update_cell(idx, 2, score)
            return score
    return None

# define a function to clear the user screen

def clear():

    os.system('cls' if os.name == 'nt' else 'clear')


def play_game():

    global wrong_answers

    end_of_game = False


    # Create a variable called 'lives' to keep track of the number of lives 
    # left. 
    # Set 'lives' to equal 6.

    lives = 6
    # Create blanks to illustrate blank word choice
    display = []
    for _ in range(word_length):
        display += "_"

    you_chose = []
    

    # loop to keep game going while condition 'end_of_game' is equal to False

    while not end_of_game:

        print(' '.join(display))

        guess = input("Guess a letter: ").lower()
        clear()

        if guess in you_chose:
            print(f"You chose {guess}. You already guessed that.")
        else:
            you_chose.append(guess)

        if guess not in chosen_word:
            print(f"You chose {guess}. That's not in the word. You lose a life!")
            wrong_answers += 1
        print(wrong_answers)

        # Check guessed letter
        for position in range(word_length):
            letter = chosen_word[position]
            
            if letter == guess:
                display[position] = letter

        # If guess is not a letter in the chosen_word, 
        # then reduce the amount of lives by 1.
        # When lives go down to 0, game is over and "You lose" is printed
        if guess not in chosen_word:
            lives -= 1
            if lives == 0:
                end_of_game = True
                print("You Lose!!")
               
        # Check if user has got all letters
        if "_" not in display:
            end_of_game = True
            print("You Win!!")
         
        # Print the ASCII art from 'stages' that corresponds to the current number of 'lives' 
        # the user has remaining
        print(stages[lives])
    
    average_score(player_name, wrong_answers)


while True:

    play_game()
    
    play_again = input("Do you want to play again? (yes/no): ").lower()

    while play_again not in ["yes", "no"]:
        print("Invalid input! Please enter 'yes' or 'no'.")
        play_again = input("Do you want to play again? (yes/no): ").lower()

    if play_again != "yes":
        break