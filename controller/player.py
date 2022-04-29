from controller.database import save_db, update_player_rank
from models.player import Player
from views.player import CreatePlayer


def create_player():

    user_entries = CreatePlayer().display_menu()

    player = Player(
        user_entries['name'],
        user_entries['firstname'],
        user_entries['birthday'],
        user_entries['gender'],
        user_entries['total_score'],
        user_entries['rating'])

    serialized_player = player.get_serialized_player()
    print(serialized_player)

    save_db("players", serialized_player)

    return player


def update_rankings(player, rank, score=True):
    if score:
        player.total_score += player.tournament_score
    player.rating = rank
    serialized_player = player.get_serialized_player()
    print(serialized_player['name'])
    update_player_rank("players", serialized_player)
    print(f"Modification du rang de {player}:\nScore total: {player.total_score}\nClassement: {player.rating}")
