# Halloween Hangman

![Halloween Hangman](https://res.cloudinary.com/dxla1usfm/image/upload/v1697459161/Project3/Am-I-Responsive_FINAL_rewqww.png)

Welcome,

Halloween Hangman is a site based on the well-known hangman game, where a user guesses a letter 
to try to figure out a randomly chosen word. It was built for online gaming enthusiast, 
who also have a love for spelling and guessing games.  

This is an excellent tool for parents, wishing to instruct their children in the practice of spelling and word comprehension.
Feeling lucky? Want to prove your skill at spelling and language comprehension? Give it a try!

You can view the live site [here](https://halloween-hangman-39dd7d1da1da.herokuapp.com/)

## Features

- Game Logic
    - user is asked to input their name. This is used to store a user_name value to the external CSV sheet using the gspread module
    - user is asked if they would like to view game statistics of the last 10 players
        - if the user choice is yes, they are presented with the running list of last 10 players, their score , amount 
        of games played and total amount of wrong answers per player.
        - if the user choice is no, they are brought within the main game loop and asked to guess a letter.
        - the user is presented with a blank underscore "_" representation of the randomly-chosen word.
    - Upon guessing their first letter, the game logic iterates through the randomly-chosen word.
        - if the letter the user chose is contained within the chosen word, the empty place-holder word is populated with
        their letter choice.
        - if the letter is not contained within the chosen_word, the user is informed of their mistake and 1 life is deducted
        from their total 6 lives.
        - if the user is able to successfully guess the chosen_word, they are informed of this and a printout of
        their total_wrong_answers and games_played is shown to them, along with the declaration of the correct word.
        - if the user loses thier 6 lives, the correct word is shown to them, they are informed of their mistake,
        and the game round exits. 
    - The user is asked if they would like to play another game.
        - if the user answers in the affirmative, they are taken back through the game loop.
        - if the user answers no, the game completely exits
- Halloween Hangman Flowchart Simplified:
    - ![Design Flow](https://res.cloudinary.com/dxla1usfm/image/upload/v1697462254/Project3/hangman_flow_chart_simplified_bb3afg.png)

### Features left to implement

- Ability for users to reset their game statistics, if desired

## Testing

- ing across various viewport sizes
    - it was confirmed that the hangman game is responsive across multiple screen sizes. This was
    accomplished via playing the game on mobile, pad and desktop computer under various screen resolutions

### Testing game features and logic

- Input and Outputs
    - painstaking confirmation, via pylint Code Institute linter was done to ensure that no code line over-exceeded
    the PEP8 specifications. Were applicable, f-strings within input/output print statements were modeled
    so as to make the user-experience seamless, in how the gaming questions appear on-screen.
- view_game_stats 
    - This function properly iterates via for loop through the user data to provide the player with 
    the last 10 players of the game. It is confirmed that if there has not been 10 players, it will out-
    put what it can access via the excel spreadsheet [hangman spreadsheet](https://docs.google.com/spreadsheets/d/1Lsa7wQwv7GQofjW7nQrEBdbmvGwen3nzPurr7diimTs/edit?pli=1#gid=460879778)
    - ### Hangman remote spreadsheet:
        - ![spreadsheet](https://res.cloudinary.com/dxla1usfm/image/upload/v1697452135/Project3/hangman_user_scores-Google-Sheets_vex3vp.png)
    - As can be seen in the above graphic, some user information is missing from the score column. This was due to contant bug 
    reworkings, in order that the proper score could be tabulated. The 'score' variable is tabulated as follows:
    score = total_wrong_answers / games_played
    - Where 2 players have the same score, the average of wrong answers is considered in order for the user with
    the least amount of wrong answers to be placed on the 'hilltop' sheet and their top score is shown to new users
    upon the initiation of game play. 
- update_hilltop_data
    - possibly the most difficult of the various functions, this method correctly retrieves information from the hangman
    spreadsheet and compares to the current player statistics. If there is no hilltop(high scorer) upon entering a game,
    this function places the current player information on the 'hilltop' sheet as the high score. Problems that were 
    originally encountered centered on global variables and total_wrong_answer giving abnormal behavior. Other problems
    were found in total_wrong_answers and games_played incrementing abnormally. Once 'duplicate' increment statements
    were found and omitted, this function was able to work as expected.
- get_and_update_games_played
    - this function is straigh-forward in its approach and is confirmed to work as expected, through trial and error. 
    It verifies if the current user has pre-existing records and, if so, helps to maintain a running count of games played.
- average_score
    - This functions main goal is to calculate the average score logic in order that the program can properly tabulate 
    this data and add it to the hangman spreadsheet for record. It utilizes a for loop to iterate through the 
    scores/players in the sheet, verify a possible match with the current user, and perform the calculation for the average 
    score. A problem that was resolved is that it used to update the title column with the player information. Once the 
    proper row was identified in the for loop, this function is confirmed to work as expected.
- clear 
    - This function successfully clears the screen, allowing the user to concentrate on the
    gameplay, minus the previous welcome screen.
- play_game
    - This is the main gameply function that successfully orchestrates a while loop
    keeping the player in gameplay until the user decides to quit. The functionality
    to continue playing has been tested and confirmed to be operating normally.
- initialize_game
    - Tested the introductory game logic that brings the user within the game. The
    questions regarding username and the ability to view the game high score all work
    as expected.
- main
    - The main function is tested and works as expected, to call the intialize game function to 
    start the player off within the game.

## Validator Testing

- W3Schools HTML and CSS validators where used to verify code integrity:

![HTML Validation](https://res.cloudinary.com/dxla1usfm/image/upload/v1697463201/Project3/Showing-results-for-https-halloween-hangman-39dd7d1da1da-herokuapp-com-Nu-Html-Checker_knhyw9.png)

![CSS Validation](https://res.cloudinary.com/dxla1usfm/image/upload/v1697463271/Project3/W3C-CSS-Validator-results-for-https-halloween-hangman-39dd7d1da1da-herokuapp-com-CSS-level-3-SVG-_pk2icu.png)



