-- Supprimer les tables si elles existent déjà
DROP TABLE IF EXISTS livres;
DROP TABLE IF EXISTS emprunts;
DROP TABLE IF EXISTS utilisateurs;

-- Création de la table livres
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite >= 0)
);

-- Création de la table emprunts
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    id_livre INTEGER NOT NULL,
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_retour TIMESTAMP NULL,
    FOREIGN KEY (id_client) REFERENCES clients(id) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES livres(id) ON DELETE CASCADE
);

-- Création de la table utilisateurs
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- Haché en production
    role TEXT CHECK (role IN ('admin', 'utilisateur')) NOT NULL DEFAULT 'utilisateur'
);

-- Création des index sur la table emprunts pour optimiser les recherches
CREATE INDEX idx_client ON emprunts(id_client);
CREATE INDEX idx_livre ON emprunts(id_livre);
