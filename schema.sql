DROP TABLE IF EXISTS livres;
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    genre TEXT NOT NULL,
    disponible TEXT NOT NULL DEFAULT 'oui'
);

DROP TABLE IF EXISTS emprunts;
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_retour TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (livre_id) REFERENCES livres(id)
);
