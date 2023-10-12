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

# Function to view game statistics

def view_game_stats():
    #Function to display game statistics of the last 10 players.
    print("\nGame Stats of the Last 10 Players:")
    print("-----------------------------------")
    
    # Display only the last 10 players
    
    user_data = data[-10:]

    for user in user_data:

        username, score, games_played, total_wrong_answers = user
        print(f"Name: {username}, Score: {score}, Games Played: {games_played}, Wrong Answers: {total_wrong_answers}")

# Function to get or update the number of games played

def update_hilltop_score(player_name, total_wrong_answers, games_played):

    # Print the updated total wrong answers and games played
    print(f"Total Wrong Answers: {total_wrong_answers}, \
        Games Played: {games_played}")

    # Calculate the new score

    new_score = 0
    
    if games_played > 0:

        new_score = total_wrong_answers / games_played
    else:
        new_score = 0

    # Concentrate only on the first row and update hilltop sheet

    current_top_row = 2
    current_best_score = hilltop.cell(current_top_row, 2).value

    # Convert current_best_score to a float if it's not None
    if current_best_score is not None:
        current_best_score_float = float(current_best_score)
    else:
        current_best_score_float = 0.0

    if not current_best_score or new_score < current_best_score_float:
        # Update 'hilltop' sheet
        hilltop.update_cell(current_top_row, 1, player_name)
        hilltop.update_cell(current_top_row, 2, str(new_score))


def get_and_update_games_played(player_name):
    
    records = gamers.get_all_records()

    # Searching for the player's record
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            new_games_played = record['games_played'] + 1
            gamers.update_cell(idx, 3, new_games_played)
            return new_games_played

    # If player is not found, add them to the sheet with 1 game played and return 1
    gamers.append_row([player_name, None, 1, 0])
    return 1

word_list = word_list
chosen_word = random.choice(word_list)
word_length = len(chosen_word)
player_name = input("What is your name?: ")
games_played = 0
wrong_answers = 0
score = 0
total_wrong_answers = 0



# Function to calculate average score
def average_score(player_name, total_wrong_answers=0):
    records = gamers.get_all_records()
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            games_played = record['games_played']
            score = total_wrong_answers / games_played
            print(score)
            print(games_played)
            print(total_wrong_answers)
            gamers.update_cell(idx, 4, total_wrong_answers)
            gamers.update_cell(idx, 2, score)
            return score
    return None

# define a function to clear the user screen

def clear():

    os.system('cls' if os.name == 'nt' else 'clear')

# Prompt user to view game stats

view_stats = input("Would you like to view game stats of the last 10 players? (yes/no): ").lower()


if view_stats == "yes":
    view_game_stats()


def play_game():

    global total_wrong_answers

    end_of_game = False

    # Create a variable called 'lives' to keep track of the number of lives 
    # left. 
    # Set 'lives' to equal 6.

    lives = 6
    wrong_answers = 0
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
    
    total_wrong_answers += wrong_answers

while True:
    games_played = get_and_update_games_played(player_name)
    
    play_game()

    # After each game, update the number of games played
    games_played += 1

    average_score(player_name, total_wrong_answers)
    update_hilltop_score(player_name, total_wrong_answers, games_played)
    
    play_again = input("Do you want to play again? (yes/no): ").lower()

    while play_again not in ["yes", "no"]:
        print("Invalid input! Please enter 'yes' or 'no'.")
        play_again = input("Do you want to play again? (yes/no): ").lower()

    if play_again != "yes":
        break

print("Thanks for playing!")
