from flask import Flask, render_template, jsonify, request, redirect, url_for, session
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

@app.route('/livres')
def livres():
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    livres = cursor.fetchall()
    conn.close()
    return render_template('afficher_livres.html', livres=livres)

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

@app.route('/emprunts', methods=['POST'])
def emprunter_livre():
    data = request.get_json()
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emprunts (id_client, id_livre) VALUES (?, ?)', (data['id_client'], data['id_livre']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Livre emprunté avec succès"}), 201

@app.route('/emprunts/<int:id>', methods=['PUT'])
def retourner_livre(id):
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE emprunts SET date_retour = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Livre retourné avec succès"})

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
