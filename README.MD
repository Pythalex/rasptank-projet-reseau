Trinome:

BONIN Alexandre

    -> majoritairement le code serveur + protocole

ELANBARI Anass

    -> majoritairement montage + client robot

ROUFF Simon

    -> majoritairement montage du robot + mise en place du raspberry + partie code serveur

Passage N°2 avec bonus/malus avec notre serveur
-> arrivé 2e (roue pétée)

Scripts:

serveur : 

    python3 webserver.py

robot : mettre clientrobot.py dans ~/adept_rasptank/server/

    sudo python3 server.py
    python3 clientrobot.py robotswag 10.42.0.137

controlleur:

    python clientpc.py robotswag 10.42.0.137


Les machines doivent être sur le même réseau/access point.
