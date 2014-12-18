import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), "../"))
from easygui_qt import easygui_qt as eg
from random import randint


def guessing_game():
    name = eg.text_input(message="What is your name?",
                            title="Mine is Reeborg.")
    if not name:
        name = "Unknown person"

    message = """<p>The following language selection will only affect the
        default GUI elements like the text on the buttons.
        Note that <b>Default</b> is reverting back to the
        local PyQt default (likely English).</p>"""

    eg.message_box(message=message, title="For information")
    eg.select_language()

    eg.message_box(message="If the text is too small or too large," +
                      " you can fix that",
                      title="For information")
    eg.set_global_font()
    eg.message_box(message="Hello {}. Let's play a game".format(name),
                      title="Guessing game!")

    guess = min_ = 1
    max_ = 50
    answer = randint(min_, max_)
    title = "Guessing game"
    while guess != answer:
        message = "Guess a number between {} and {}".format(min_, max_)
        prev_guess = guess
        guess = eg.integer_input(message=message, title=title,
                              default_value=guess, min_=min_ ,max_=max_)
        if guess is None:
            quitting = eg.yes_no_question("Do you want to quit?")
            guess = prev_guess
            if quitting:
                break
        elif guess < answer:
            title = "Too low"
            min_ = guess
        elif guess > answer:
            title = "Too high"
            max_ = guess
    else:
        message="Congratulations {}! {} was the answer.".format(name, guess)
        eg.message_box(message, title="You win!")


if __name__ == '__main__':
    eg.message_box("Temporarily setting the locale to Spanish")
    eg.set_locale('es')
    guessing_game()

