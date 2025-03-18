import sqlite3

connection = sqlite3.connect('bibliotheque.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cur.execute("INSERT INTO utilisateurs (username, password, role) VALUES (?, ?, ?)", ('user1', 'userpass', 'utilisateur'))

cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ('Orgueil et Préjugés', 'Jane Austen'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ('Le Rouge et le Noir', 'Stendhal'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ('1984', 'George Orwell'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ("L'Étranger", 'Albert Camus'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ("Jacques La Fatalis", 'Diderot'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ("Le Petit Prince", 'Antoine de Saint-Exupéry'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ("Harry Potter à l'école des sorciers", 'J.K. Rowling'))
cur.execute("INSERT INTO livres (titre, auteur ) VALUES (?, ?)", ("Les Misérables", 'Victor Hugo'))

connection.commit()
connection.close()
