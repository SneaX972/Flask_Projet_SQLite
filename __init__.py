from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

# Modèle Livre
class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    disponible = db.Column(db.Boolean, default=True)

# Modèle Utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

# Modèle Emprunt
class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', backref=db.backref('emprunts', lazy=True))
    livre = db.relationship('Livre', backref=db.backref('emprunts', lazy=True))

@app.route('/')
def index():
    livres = Livre.query.all()
    return render_template('index.html', livres=livres)

@app.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    nouveau_livre = Livre(titre=titre, auteur=auteur)
    db.session.add(nouveau_livre)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    livre = Livre.query.get(id)
    if livre:
        db.session.delete(livre)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/emprunter/<int:livre_id>/<int:utilisateur_id>')
def emprunter_livre(livre_id, utilisateur_id):
    livre = Livre.query.get(livre_id)
    utilisateur = Utilisateur.query.get(utilisateur_id)
    if livre and utilisateur and livre.disponible:
        livre.disponible = False
        emprunt = Emprunt(utilisateur_id=utilisateur_id, livre_id=livre_id)
        db.session.add(emprunt)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/retourner/<int:livre_id>')
def retourner_livre(livre_id):
    livre = Livre.query.get(livre_id)
    emprunt = Emprunt.query.filter_by(livre_id=livre_id).first()
    if livre and emprunt:
        livre.disponible = True
        db.session.delete(emprunt)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
