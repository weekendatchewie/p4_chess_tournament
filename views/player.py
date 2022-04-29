from views.view import View
from controller.database import load_db


class CreatePlayer(View):

    def display_menu(self):
        name = input("Nom du joueur :\n"
                     ">>> ")

        firstname = input("Prénom du joueur :\n"
                          ">>> ")

        birthday = self.get_user_entry(
            msg_display="Date de naissance (format DD/MM/YYYY) :\n"
                        ">>> ",
            msg_error="Veuillez entrer une date au format valide: DD/MM/YYYY",
            value_type="date"
        )

        gender = self.get_user_entry(
            msg_display="Sexe (H ou F) :\n"
                        ">>> ",
            msg_error="Veuillez entrer H ou F",
            value_type="selection",
            assertions=["H", "h", "F", "f"]
        ).upper()

        rating = self.get_user_entry(
            msg_display="Classement :\n"
                        ">>> ",
            msg_error="Veuillez entrer une valeur numérique valide",
            value_type="numeric"
        )

        print(f"{firstname} {name} a été créé")

        return {
            "name": name,
            "firstname": firstname,
            "birthday": birthday,
            "gender": gender,
            "total_score": 0,
            "rating": rating,
        }


class LoadPlayer(View):

    def display_menu(self, nb_players_to_load):

        all_players = load_db("players")
        serialized_loaded_players = []
        for i in range(nb_players_to_load):
            print(f"Plus que {str(nb_players_to_load - i)} joueur(s) à charger")
            display_msg = "Choisir un joueur :\n"

            assertions = []
            for j, player in enumerate(all_players):
                display_msg = display_msg + f"{str(j + 1)} - {player['firstname']} {player['name']}\n"
                assertions.append(str(j + 1))

            user_input = int(self.get_user_entry(
                msg_display=f"{display_msg}\n"
                            ">>> ",
                msg_error="Veuillez entrer un nombre entier.",
                value_type="selection",
                assertions=assertions
            ))
            if all_players[user_input - 1] not in serialized_loaded_players:
                serialized_loaded_players.append(all_players[user_input - 1])
            else:
                print("Joueur déjà chargé. Merci de choisir un autre joueur.")
                nb_players_to_load += 1

        return serialized_loaded_players
