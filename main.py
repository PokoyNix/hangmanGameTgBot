from app.core.game import HangmanGame

game = HangmanGame("python")

print(game.masked_word())

while not game.is_finished():
    letter = input("Enter a letter: ")
    result = game.guess(letter)

    print(letter)
    print(game.masked_word())
    print("Attempts:", game.attempts_left())

print("Game finished:", game.status())

