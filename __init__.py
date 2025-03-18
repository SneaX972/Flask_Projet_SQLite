from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('authentification'))

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM utilisateurs WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and user['password'] == password:  # Comparaison du mot de passe en clair
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    return render_template('dashboard.html', role=session['role'])

@app.route('/livres', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    quantite = request.form['quantite']

    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livres (titre, auteur, quantite) VALUES (?, ?, ?)', (titre, auteur, quantite))
    conn.commit()
    conn.close()

    return redirect(url_for('afficher_livres'))

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, quantite) VALUES (?, ?, ?)', (titre, auteur, 1))  # Ajout de quantite
        conn.commit()
        conn.close()
        return redirect(url_for('livres'))
    return render_template('ajouter_livre.html')  # Renommé en ajouter_livre.html

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('livres'))

@app.route('/emprunter_livre/<int:id>')
def emprunter_livre(id):
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    conn = get_db_connection()
    conn.execute('INSERT INTO emprunts (id_client, id_livre) VALUES (?, ?)', (session['user_id'], id))  # Utilisation des bons noms de colonnes
    conn.execute('UPDATE livres SET quantite = quantite - 1 WHERE id = ?', (id,))  # Decrémenter la quantité
    conn.commit()
    conn.close()
    return redirect(url_for('livres'))

@app.route('/retourner_livre/<int:id>')
def retourner_livre(id):
    if 'user_id' not in session:
        return redirect(url_for('authentification'))
    conn = get_db_connection()
    conn.execute('DELETE FROM emprunts WHERE id_client = ? AND id_livre = ?', (session['user_id'], id))  # Utilisation des bons noms de colonnes
    conn.execute('UPDATE livres SET quantite = quantite + 1 WHERE id = ?', (id,))  # Incrémenter la quantité
    conn.commit()
    conn.close()
    return redirect(url_for('livres'))

@app.route('/utilisateurs')
def utilisateurs():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM utilisateurs').fetchall()
    conn.close()
    return render_template('utilisateurs.html', utilisateurs=users)

@app.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
