import sqlite3

connection = sqlite3.connect('bibliotheque.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'userpass', 'utilisateur'))

cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ('Orgueil et Préjugés', 'Jane Austen', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ('Le Rouge et le Noir', 'Stendhal', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ("L'Étranger", 'Albert Camus', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ("Jacques La Fatalis", 'Diderot', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ("Le Petit Prince", 'Antoine de Saint-Exupéry', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 1))
cur.execute("INSERT INTO livres (titre, auteur, quantité) VALUES (?, ?, ?)", ("Les Misérables", 'Victor Hugo', 1))

connection.commit()
connection.close()
