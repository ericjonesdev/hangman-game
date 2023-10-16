# Halloween Hangman

![Halloween Hangman](https://res.cloudinary.com/dxla1usfm/image/upload/v1697459161/Project3/Am-I-Responsive_FINAL_rewqww.png)

Welcome,

Halloween Hangman is a site based on the well-known hangman game, where a user guesses a letter 
to try to figure out a randomly chosen word. It was built for online gaming enthusiast, 
who also have a love for spelling and guessing games.  

This is an excellent tool for parents, wishing to instruct their children in the practice of spelling and word comprehension.
Feeling lucky? Want to prove your skill at spelling and language comprehension? Give it a try!

You can view the live site [here](https://halloween-hangman-39dd7d1da1da.herokuapp.com/)

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
