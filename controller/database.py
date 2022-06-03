from pathlib import Path

from tinydb import TinyDB
from tinydb import where

from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


def save_db(db_name, serialized_data):
    Path("data/").mkdir(exist_ok=True)
    try:
        db = TinyDB(f"data/{db_name}.json")
    except FileNotFoundError:
        with open(f"data/{db_name}.json", "w"):
            pass
        db = TinyDB("data/" + db_name + ".json")

    db.insert(serialized_data)
    print(f"{serialized_data['name']} sauvegardé avec succès.")


def update_db(db_name, serialized_data):
    db = TinyDB(f"data/{db_name}.json")
    db.update(
        serialized_data,
        where('name') == serialized_data['name']
    )
    print(f"{serialized_data['name']} modifié avec succès.")


def update_player_rank(db_name, serialized_data):
    db = TinyDB(f"data/{db_name}.json")
    db.update(
            {'rating': serialized_data['rating'], 'total_score': serialized_data['total_score']},
            where('name') == serialized_data['name']
    )
    print(f"{serialized_data['name']} modifié avec succès.")


def load_db(db_name):
    if not Path("data/").exists():
        Path("data/").mkdir()
    db = TinyDB(f"data/{db_name}.json")
    return db.all()


def load_player(serialized_player, load_tournament_score=False):
    player = Player(
        serialized_player["name"],
        serialized_player["firstname"],
        serialized_player["birthday"],
        serialized_player["gender"],
        serialized_player["rating"],
        serialized_player["total_score"],
    )
    if load_tournament_score:
        player.tournament_score = serialized_player["tournament_score"]
    return player


def load_tournament(serialized_tournament):
    loaded_tournament = Tournament(
        serialized_tournament["name"],
        serialized_tournament["location"],
        serialized_tournament["date"],
        serialized_tournament["time_control"],
        [load_player(player, load_tournament_score=True) for player in serialized_tournament["players"]],
        serialized_tournament["rounds_number"],
        serialized_tournament["description"]
    )
    loaded_tournament.rounds = load_rounds(serialized_tournament, loaded_tournament)

    return loaded_tournament


def load_rounds(serialized_tournament, tournament):

    loaded_rounds = []

    for rd in serialized_tournament["list_round"]:
        players_pairs = []
        pair_p1 = None
        pair_p2 = None
        for pair in rd["players_pairs"]:
            for player in tournament.players:
                if player.name == pair[0]["name"]:
                    pair_p1 = player
                elif player.name == pair[1]["name"]:
                    pair_p2 = player
            players_pairs.append((pair_p1, pair_p2))
        loaded_round = Round(
            rd["name"],
            players_pairs,
            load_match=True
        )
        loaded_round.matchs = [load_match(match, tournament) for match in rd["matchs"]]
        loaded_round.start_date = rd["start_date"]
        loaded_round.end_date = rd["end_date"]
        loaded_rounds.append(loaded_round)

    return loaded_rounds


def load_match(serialized_match, tournament):

    player_1 = None
    player_2 = None

    for player in tournament.players:
        if player.name == serialized_match["player_1"]["name"]:
            player_1 = player
        elif player.name == serialized_match["player_2"]["name"]:
            player_2 = player

    loaded_match = Match(player_1, player_2, serialized_match['name'])
    loaded_match.score_player_1 = serialized_match["score_player_1"]
    loaded_match.score_player_2 = serialized_match["score_player_2"]
    loaded_match.winner = serialized_match["winner"]

    return loaded_match
