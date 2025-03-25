import sqlite3

# Connexion à la base de données spécifique à la bibliothèque
connection = sqlite3.connect('bibliotheque.db')

# Lecture et exécution du fichier SQL dédié aux livres et emprunts
with open('schema.sql') as f:
    connection.executescript(f.read())

# Ajouter un utilisateur adminn
cur.execute("""
INSERT INTO Utilisateurs (Canta, Nico, Email, Mot_de_passe, Role)
VALUES (?, ?, ?, ?, ?)
""", ('Admin', 'Super', 'test@biblio.com', 'password', 'admin'))

cur = connection.cursor()

# Remplissage initial des livres
cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Conte philosophique', 'oui'))

cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('Les Misérables', 'Victor Hugo', 'Roman historique', 'oui'))

cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('1984', 'George Orwell', 'Science-fiction', 'oui'))

cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantasy', 'oui'))

cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('L\'Étranger', 'Albert Camus', 'Roman', 'oui'))

cur.execute("INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)",
            ('Voyage au bout de la nuit', 'Louis-Ferdinand Céline', 'Roman', 'oui'))

connection.commit()
connection.close()
