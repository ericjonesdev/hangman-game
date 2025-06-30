import gspread
from google.oauth2.service_account import Credentials
from hangman_art import stages, logo
from hangman_words import word_list
import random
import os
import sys
import json

def get_input(prompt, input_type="text"):
    """
    Universal input handler with strict validation
    input_type: "text" (for names), "yn" (for yes/no), or "letter" (for guesses)
    """
    try:
        response = input(prompt).strip().lower()
        
        if input_type == "yn":
            return "yes" if response in ("yes", "y") else "no"
        elif input_type == "letter":
            if len(response) == 1 and response.isalpha():
                return response
            return None  # Force re-prompt
        return response or "Player1"  # Default for text input
    except Exception:
        return None  # Return None on any error

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds_json = os.getenv('GOOGLE_CREDS')
if not creds_json:
    print("ERROR: Google Sheets credentials not found!")
    sys.exit(1)

try:
    # Changed from from_service_account_FILE to from_service_account_INFO
    CREDS = Credentials.from_service_account_info(json.loads(creds_json))
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('hangman_user_scores')
except Exception as e:
    print(f"Failed to connect to Google Sheets: {str(e)}")
    sys.exit(1)

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
    print(f"Total Wrong Answers: {total_wrong_answers}, Games Played: {games_played}")

    new_score = total_wrong_answers / games_played if games_played > 0 else 0
    hilltop_data = hilltop.get_all_records()

    if not hilltop_data:
        hilltop.append_row([player_name, new_score])
        return

    min_score = float('inf')
    min_score_player = None

    for player in hilltop_data:
        if float(player['high_score']) < min_score:
            min_score = float(player['high_score'])
            min_score_player = player['user_name']
        elif float(player['high_score']) == min_score:
            for record in data:
                if record[0] == player['user_name']:
                    other_player_avg = int(record[3]) / int(record[2])
                    current_player_avg = total_wrong_answers / games_played
                    if current_player_avg < other_player_avg:
                        min_score = new_score
                        min_score_player = player_name

    if new_score <= min_score:
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
    for idx, record in enumerate(records, start=2):
        if record['username'] == player_name:
            new_games_played = record['games_played'] + 1
            gamers.update_cell(idx, 3, new_games_played)
            return new_games_played

    gamers.append_row([player_name, None, 1, 0])
    return 1

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
    guessed_letters = []

    while not end_of_game and lives > 0:
        print('\n' + ' '.join(display))
        print(stages[lives])

        while True:
            guess = get_input("Guess a letter: ", "letter")
            if guess is None:
                print("Invalid input. Please try again.")
                continue
            if guess in guessed_letters:
                print(f"You already guessed '{guess}'. Try a different letter.")
                continue
            break

        guessed_letters.append(guess)
        clear()

        if guess in chosen_word:
            print(f"Good guess! '{guess}' is in the word.")
            for position in range(word_length):
                if chosen_word[position] == guess:
                    display[position] = guess
        else:
            print(f"Sorry, '{guess}' is not in the word. You lose a life!")
            lives -= 1
            wrong_answers += 1

        if "_" not in display:
            end_of_game = True
            print(f"Congratulations! You guessed: {chosen_word}")

    if lives <= 0:
        print(f"Game over! The word was: {chosen_word}")

    total_wrong_answers += wrong_answers

def initialize_game():
    global player_name, total_wrong_answers
    
    print(logo)
    
    try:
        if len(data2) > 1:
            player = hilltop.col_values(1)[1]
            high_score = hilltop.col_values(2)[1]
            print(f"Top Scorer: {player} Score: {high_score}")
        else:
            print("No high scores yet!")
    except Exception as e:
        print(f"Couldn't load high scores: {str(e)}")
    
    player_name = get_input("What is your name?:\n", "text")
    print(f"Welcome, {player_name}!")
    
    while True:
        view_stats = get_input("View last 10 players' stats? (yes/no):\n", "yn")
        if view_stats == "yes":
            view_game_stats()
            break
        elif view_stats == "no":
            break
        print("Please answer 'yes' or 'no'.")

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
            play_again = get_input("Do you want to play again? (yes/no):\n ").lower()

        if play_again != "yes":
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()