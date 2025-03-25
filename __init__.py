from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                  

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/administration')
def administration():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return render_template('administration.html')


@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return redirect(url_for('administration'))

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('administration'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/gestion_utilisateurs', methods=['GET', 'POST'])
def gestion_utilisateurs():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']

        cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, adresse))
        conn.commit()

    cursor.execute('SELECT * FROM clients;')
    utilisateurs = cursor.fetchall()

    conn_bib = sqlite3.connect('bibliotheque.db')
    cursor_bib = conn_bib.cursor()

    utilisateurs_avec_livres = []
    for utilisateur in utilisateurs:
        cursor_bib.execute('''SELECT livres.titre FROM emprunts
                            JOIN livres ON emprunts.livre_id = livres.id
                            WHERE emprunts.client_id = ? AND emprunts.date_retour IS NULL''', (utilisateur[0],))
        livres_empruntes = cursor_bib.fetchall()
        utilisateurs_avec_livres.append((utilisateur, livres_empruntes))

    conn.close()
    conn_bib.close()

    return render_template('gestion_utilisateurs.html', utilisateurs_avec_livres=utilisateurs_avec_livres)

@app.route('/recherche_livres', methods=['GET', 'POST'])
def recherche_livres():
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        recherche = request.form['recherche']
        cursor.execute('SELECT * FROM livres WHERE disponible = "oui" AND titre LIKE ?', ('%' + recherche + '%',))
    else:
        cursor.execute('SELECT * FROM livres WHERE disponible = "oui"')

    livres = cursor.fetchall()
    conn.close()
    return render_template('recherche_livres.html', livres=livres)

@app.route('/supprimer_utilisateur/<int:id>', methods=['POST'])
def supprimer_utilisateur(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/gestion_utilisateurs')

@app.route('/consultation_livres')
def consultation_livres():
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    livres = cursor.fetchall()
    conn.close()
    return render_template('liste_livres.html', livres=livres)


@app.route('/emprunter_livre', methods=['POST'])
def emprunter_livre():
    client_id = request.form['client_id']
    livre_id = request.form['livre_id']

    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emprunts (client_id, livre_id) VALUES (?, ?)', (client_id, livre_id))
    cursor.execute('UPDATE livres SET disponible = "non" WHERE id = ?', (livre_id,))
    conn.commit()
    conn.close()
    return redirect('/recherche_livres')

@app.route('/retourner_livre', methods=['POST'])
def retourner_livre():
    livre_id = request.form['livre_id']

    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE emprunts SET date_retour = CURRENT_TIMESTAMP WHERE livre_id = ? AND date_retour IS NULL', (livre_id,))
    cursor.execute('UPDATE livres SET disponible = "oui" WHERE id = ?', (livre_id,))
    conn.commit()
    conn.close()
    return redirect('/consultation_livres')


@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        disponible = request.form.get('disponible', 'oui')

        conn = sqlite3.connect('bibliotheque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livres (titre, auteur, genre, disponible) VALUES (?, ?, ?, ?)', (titre, auteur, genre, disponible))
        conn.commit()
        conn.close()
        return redirect('/consultation_livres')
    return render_template('formulaire_livre.html')

@app.route('/supprimer_livre/<int:id>', methods=['POST'])
def supprimer_livre(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/consultation_livres')

if __name__ == "__main__":
  app.run(debug=True)
