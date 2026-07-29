from app.services.game_service import GameService

service = GameService()

user_id = 1

service.start_game(user_id, "python")

while service.has_active_game(user_id):
    letter = input("Enter a letter: ")
    result = service.guess(user_id, letter)

    game = service.get_game(user_id)

    print(result)
    if game:
        print(game.masked_word())
        print("Attempts:", game.attempts_left())


