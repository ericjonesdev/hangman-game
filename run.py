import gspread
from google.oauth2.service_account import Credentials
from hangman_art import stages, logo
from hangman_words import word_list
import random
import os
import sys

def get_input(prompt, input_type="text"):
    """
    Universal input handler with strict validation
    input_type: "text" (for names), "yn" (for yes/no), or "letter" (for guesses)
    """
    max_attempts = 3  # Prevent infinite loops
    attempts = 0
    
    while attempts < max_attempts:
        try:
            print(prompt, end='', flush=True)
            response = input().strip().lower()  # Always use input()
            
            if input_type == "yn":
                if response in ("yes", "y"):
                    return "yes"
                elif response in ("no", "n"):
                    return "no"
                print("Please enter 'yes' or 'no'.")
            
            elif input_type == "letter":
                if len(response) == 1 and response.isalpha():
                    return response
                print("Please enter a single letter (a-z).")
            
            else:  # text input
                return response or "Player1"  # Default name
            
            attempts += 1
        except EOFError:  # Handle cases where input isn't available
            print("\nInput error. Using default value.")
            return "no" if input_type == "yn" else ("a" if input_type == "letter" else "Player1")
    
    # After max attempts, return a default
    return "no" if input_type == "yn" else ("a" if input_type == "letter" else "Player1")

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

def view_game_stats():

    '''
    Function to display game statistics of the last 10 players.
    '''

    print("\nGame Stats of the Last 10 Players:")
    print("-----------------------------------")

    # Display only the last 10 players

    user_data = data[-10:]

    for user in user_data:

        username, score, games_played, total_wrong_answers = user
        print(f"Name: {username}, Score: {score},"
              f" Games Played: {games_played},"
              f" Wrong Answers: {total_wrong_answers}")


def update_hilltop_score(player_name, total_wrong_answers, games_played):

    '''
    Function to get and update the best player score
    '''

    # Print the updated total wrong answers and games played
    print(f"Total Wrong Answers: {total_wrong_answers}, \
    Games Played: {games_played}")

    # Calculate the new score
    if games_played > 0:
        new_score = total_wrong_answers / games_played
    else:
        new_score = 0

    hilltop_data = hilltop.get_all_records()

    # If hilltop sheet is empty, add the current player's data
    if not hilltop_data:
        hilltop.append_row([player_name, new_score])
        return

    # Identify the player with the lowest high_score
    min_score = float('inf')
    min_score_player = None

    for player in hilltop_data:
        if float(player['high_score']) < min_score:
            min_score = float(player['high_score'])
            min_score_player = player['user_name']
        # If two players have the same high_score, prioritize based on the
        # #average of wrong answers
        elif float(player['high_score']) == min_score:
            # Fetch the other player's total_wrong_answers and games_played
            # #from the 'gamers' sheet
            for record in data:
                if record[0] == player['user_name']:
                    other_player_avg = int(record[3]) / int(record[2])
                    current_player_avg = total_wrong_answers / games_played
                    if current_player_avg < other_player_avg:
                        min_score = new_score
                        min_score_player = player_name

    # If the current player's score is better than or equal to the lowest
    # #high_score in hilltop sheet, update the sheet
    if new_score <= min_score:
        # Find the row of the player with the lowest high_score and update it
        for i, player in enumerate(hilltop_data, start=2):
            if player['user_name'] == min_score_player:
                hilltop.update_cell(i, 1, player_name)
                hilltop.update_cell(i, 2, str(new_score))
                break


def get_and_update_games_played(player_name):

    '''
    Function to update games played
    '''

    records = gamers.get_all_records()

    # Search for the player's record
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            new_games_played = record['games_played'] + 1
            gamers.update_cell(idx, 3, new_games_played)
            return new_games_played

    # If player is not found, add them to the sheet with 1 game played
    # and return 1
    gamers.append_row([player_name, None, 1, 0])
    return 1

# Word list is pulling in words from import statement


word_list = word_list


games_played = 0
wrong_answers = 0
total_wrong_answers = 0


def average_score(player_name, total_wrong_answers=0):

    '''
    Function to calculate average score
    '''

    records = gamers.get_all_records()
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            games_played = record['games_played']
            score = total_wrong_answers / games_played
            gamers.update_cell(idx, 4, total_wrong_answers)
            gamers.update_cell(idx, 2, score)
            return score
    return None


def clear():

    '''
    Function to clear the user screen for usability
    '''

    os.system('cls' if os.name == 'nt' else 'clear')


def play_game():
    global total_wrong_answers

    chosen_word = random.choice(word_list)
    word_length = len(chosen_word)
    end_of_game = False
    lives = 6
    wrong_answers = 0
    display = ["_"] * word_length
    you_chose = []

    while not end_of_game and lives > 0:
        print(f"\n{' '.join(display)}")
        print(stages[lives])  # Show hangman art first

        guess = get_input("Guess a letter: ", "letter")
        clear()

        if not guess:  # Skip if invalid input
            continue

        if guess in you_chose:
            print(f"You already guessed '{guess}'. Try again.")
            continue

        you_chose.append(guess)

        if guess in chosen_word:
            print(f"Correct! '{guess}' is in the word.")
            for i, letter in enumerate(chosen_word):
                if letter == guess:
                    display[i] = letter
        else:
            print(f"Wrong! '{guess}' is not in the word. You lose a life.")
            lives -= 1
            wrong_answers += 1

        if "_" not in display:
            end_of_game = True
            print(f"\nYou won! The word was: {chosen_word}")
        
        if lives <= 0:
            end_of_game = True
            print(f"\nYou lost! The word was: {chosen_word}")

    total_wrong_answers += wrong_answers


def initialize_game():
    global player_name, total_wrong_answers

    print(logo)

    if len(data2) > 1:
        player = hilltop.col_values(1)[1]
        high_score = hilltop.col_values(2)[1]
        print(f"Top Scorer:-{player} Score:{high_score}")
    else:
        print("No high scores yet!")

    player_name = get_input("What is your name?:\n ", "text")

    # Initialize the total wrong answers
    total_wrong_answers = 0

    # Prompt user to view game stats - WITH VALIDATION LOOP
    while True:
        view_stats = get_input("Would you like to view game stats of the last 10 players? (yes/no):\n ", "yn")
        if view_stats == "yes":
            view_game_stats()
            break
        elif view_stats == "no":
            break


def main():
    '''
    Initialize game function
    '''

    initialize_game()

    while True:
        games_played = get_and_update_games_played(player_name)

        play_game()

        average_score(player_name, total_wrong_answers)
        update_hilltop_score(player_name, total_wrong_answers, games_played)

        play_again = get_input("Do you want to play again? (yes/no): ").lower()

        while play_again not in ["yes", "no"]:
            print("Invalid input! Please enter 'yes' or 'no'.")
            play_again = get_input("Do you want\
                 to play again? (yes/no):\n ").lower()

        if play_again != "yes":
            break

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
