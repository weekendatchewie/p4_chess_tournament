# Projet 4

- Se rendre sur le repo https://github.com/weekendatchewie/p4_chess_tournament
- Cloner ou télécharger le repo
- Créer un environnement virtuel :
    ```
    python3 -m venv venv
    ```
  
- Activer l'environnement virtuel :

    Linux/Macos :
    ```
    source venv/bin/activate
    ```
    
    Windows :
    ```
    venv\scripts\activate.bat
    ```

- Installer les packages :
    ```
    pip install -r requirements.txt
    ```

- Lancer le script :
    ```
    python main.py
    ```
  
- Générer le rapport coverage :
  ```
  flake8 --format=html --htmldir=flake-report
  ```
