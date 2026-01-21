Créer l'environnement :
```sh
python3 -m venv .ve
```

Activer l'environnement :
```sh
source .ve/bin/activate  # sous linux, macos
.vebdw\Scripts\activate  # sous windows
```

Installer les dépendances :
```sh
pip install -r requirements.in
```


Lancer l'application (localhost 8000 par défaut) :
```sh
fastapi run serveur.py
```
ou
```
fastapi dev serveur.py
```
