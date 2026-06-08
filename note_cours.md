variables d'environement : 
	+ logs (username / password)
	+ clefs api

On ne veut que les variables d'environement soient présentes dans le code source. -> n'importe quel personne qui aurait accès à notre source code pourrait voir ses identifiants et donc usurper notre identité.

En général, on les stocke dans un fichier ".env" -> dans notre source code pour avoir accès dans notre code à ses variables là on utilise la lib : "python-dotenv"
____________________________________
Une clef API est l'équivalent pour les developeurs à un username/password.
Elle donne accès à des services d'une plateforme donnée.
