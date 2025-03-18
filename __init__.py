from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

def est_admin():
    return session.get('role') == 'admin'

# Route d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM utilisateurs WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['authentifie'] = True
            session['role'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Tableau de bord
@app.route('/dashboard')
def dashboard():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return render_template('dashboard.html', admin=est_admin())

# Ajouter un livre
@app.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    if not est_admin():
        return jsonify({'error': 'Accès refusé'}), 403
    data = request.get_json()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)', 
                   (data['titre'], data['auteur'], data['stock']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre ajouté avec succès'})

# Supprimer un livre
@app.route('/supprimer_livre/<int:livre_id>', methods=['DELETE'])
def supprimer_livre(livre_id):
    if not est_admin():
        return jsonify({'error': 'Accès refusé'}), 403
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (livre_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre supprimé'})

# Rechercher un livre
@app.route('/recherche_livres', methods=['GET'])
def recherche_livres():
    query = request.args.get('query', '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE titre LIKE ? OR auteur LIKE ?', ('%' + query + '%', '%' + query + '%'))
    livres = cursor.fetchall()
    conn.close()
    return jsonify(livres)

# Emprunter un livre
@app.route('/emprunter/<int:livre_id>', methods=['POST'])
def emprunter_livre(livre_id):
    if not est_authentifie():
        return jsonify({'error': 'Non authentifié'}), 403
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE livres SET stock = stock - 1 WHERE id = ? AND stock > 0', (livre_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre emprunté'})

# Retourner un livre
@app.route('/retourner/<int:livre_id>', methods=['POST'])
def retourner_livre(livre_id):
    if not est_authentifie():
        return jsonify({'error': 'Non authentifié'}), 403
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE livres SET stock = stock + 1 WHERE id = ?', (livre_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre retourné'})

if __name__ == "__main__":
    app.run(debug=True)
