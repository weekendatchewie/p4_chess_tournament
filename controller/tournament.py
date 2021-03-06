from models.tournament import Tournament
from views.view import View
from views.tournament import CreateTournament
from views.player import LoadPlayer
from controller.player import create_player, update_rankings
from controller.database import save_db, update_db, load_player


def create_tournament():

    menu = View()
    user_entries = CreateTournament().display_menu()

    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n"
                    "0 - Créer des joueurs\n"
                    "1 - Charger des joueurs\n"
                    ">>> ",
        msg_error="Entrez un choix valide",
        value_type="selection",
        assertions=["0", "1"]
    )

    players = []

    if user_input == "1":

        print(f"Chargement de {str(user_entries['nb_players'])} joueurs")

        serialized_players = LoadPlayer().display_menu(
            nb_players_to_load=user_entries['nb_players']
        )

        for serialized_player in serialized_players:
            player = load_player(serialized_player)
            players.append(player)

    else:
        print(f"Création de {str(user_entries['nb_players'])} joueurs")

        while len(players) < user_entries['nb_players']:
            players.append(create_player())

    if not players:
        print("Il n'y a aucun joueur, veuillez en créer")
        print()
        print(f"Création de {str(user_entries['nb_players'])} joueurs")
        while len(players) < user_entries['nb_players']:
            players.append(create_player())

    tournament = Tournament(
        user_entries['name'],
        user_entries['location'],
        user_entries['date'],
        user_entries['time_control'],
        players,
        user_entries['nb_rounds'],
        user_entries['desc'])

    save_db("tournaments", tournament.get_serialized_tournament())

    return tournament


def play_tournament(tournament, new_tournament_loaded=False):

    menu = View()
    print()
    print(f"Début du tournoi {tournament.name}")
    print()

    while True:

        a = 0
        if new_tournament_loaded:
            for round in tournament.list_round:
                if round.end_date is None:
                    a += 1
            nb_rounds_to_play = tournament.rounds_number - a
            new_tournament_loaded = False
        else:
            nb_rounds_to_play = tournament.rounds_number

        for i in range(nb_rounds_to_play):

            tournament.create_round(round_number=i+a)

            current_round = tournament.list_round[-1]
            print(f"{current_round.start_date} : Début du {current_round.name}")

            while True:
                print()
                user_input = menu.get_user_entry(
                    msg_display="Faîtes votre choix :\n"
                                "0 - Round suivant\n"
                                "1 - Voir les classements\n"
                                "2 - Mettre à jour les classements\n"
                                "3 - Sauvegarder le tournoi\n"
                                "Q - Quitter\n"
                                ">>> ",
                    msg_error="Veuillez faire un choix.",
                    value_type="selection",
                    assertions=["0", "1", "2", "3", "q", "Q"]
                )

                if user_input == "0":
                    current_round.mark_as_complete()
                    break

                elif user_input == "1":
                    print(f"Classement du tournoi {tournament.name} :\n")
                    for j, player in enumerate(tournament.get_rankings()):
                        print(f"{str(j + 1)} - {player}")

                elif user_input == "2":
                    for player in tournament.players:
                        rank = menu.get_user_entry(
                            msg_display=f"Rang de {player}:\n>>> ",
                            msg_error="Veuillez entrer un nombre entier.",
                            value_type="numeric"
                        )
                        update_rankings(player, rank, score=False)

                elif user_input == "3":
                    rankings = tournament.get_rankings()
                    for j, player in enumerate(rankings):
                        for t_player in tournament.players:
                            if player.name == t_player.name:
                                t_player.rank = str(j + 1)
                    update_db("tournaments", tournament.get_serialized_tournament(save_rounds=True))

                elif user_input.upper() == "Q":
                    quit()

            if new_tournament_loaded:
                break

        if new_tournament_loaded:
            continue

        else:
            break

    rankings = tournament.get_rankings()
    for i, player in enumerate(rankings):
        for t_player in tournament.players:
            if player.name == t_player.name:
                t_player.total_score += player.tournament_score
                t_player.rating = str(i+1)
    update_db("tournaments", tournament.get_serialized_tournament(save_rounds=True))

    return rankings
