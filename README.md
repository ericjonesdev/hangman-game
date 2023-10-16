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

- Testing across various viewport sizes
    - it was confirmed that the hangman game is responsive across multiple screen sizes. This was
    accomplished via playing the game on mobile, pad and desktop computer under various screen resolutions

### Testing game features and logic

- Input and Outputs
    - painstaking confirmation, via pylint Code Institute linter was done to ensure that no code line over-exceeded
    the PEP8 specifications. Were applicable, f-strings within input/output print statements were modeled
    so as to make the user-experience seamless, in how the gaming questions appear on-screen.
    

