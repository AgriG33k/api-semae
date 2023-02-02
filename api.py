from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME')
)

db = SQLAlchemy(app)

class Varieties(db.Model):
    __tablename__ = os.getenv('DB_TABLE')
    id_espece = db.Column(db.String(255))
    espece = db.Column(db.String(255))
    id_variete = db.Column(db.String(255))
    variete = db.Column(db.String(255))
    liste = db.Column(db.String(255))
    obtenteur = db.Column(db.String(255))
    annee_inscription = db.Column(db.Integer)
    date_inscription = db.Column(db.Date)
    informations_complementaires = db.Column(db.Text)
    typ_var1 = db.Column(db.String(255))
    typ_var2 = db.Column(db.String(255))
    typ_var3 = db.Column(db.String(255))
    typ_var4 = db.Column(db.String(255))
    typ_var5 = db.Column(db.String(255))
    code_gnis = db.Column(db.String(255),primary_key=True)
    
    def __init__(self, id_espece, espece, id_variete, variete, liste, obtenteur, annee_inscription, date_inscription, informations_complementaires, typ_var1, typ_var2, typ_var3, typ_var4, typ_var5, code_gnis):
        self.id_espece = id_espece
        self.espece = espece
        self.id_variete = id_variete
        self.variete = variete
        self.liste = liste
        self.obtenteur = obtenteur
        self.annee_inscription = annee_inscription
        self.date_inscription = date_inscription
        self.informations_complementaires = informations_complementaires
        self.typ_var1 = typ_var1
        self.typ_var2 = typ_var2
        self.typ_var3 = typ_var3
        self.typ_var4 = typ_var4
        self.typ_var5 = typ_var5
        self.code_gnis = code_gnis

@app.route('/varietes', methods=['GET'])
def get_varietes():
    id_espece = request.args.get('id_espece')
    nom_variete = request.args.get('nom_variete')
    obtenteur = request.args.get('obtenteur')
    liste = request.args.get('liste')

    varietes = Varieties.query.order_by(Varieties.variete)
    if id_espece:
        varietes = varietes.filter(Varieties.id_espece == id_espece)
        
    if nom_variete:
        varietes = varietes.filter(Varieties.variete.like('%' + nom_variete + '%'))
    
    if obtenteur:
        varietes = varietes.filter(Varieties.obtenteur.like('%' + obtenteur + '%'))
    
    if liste:
        varietes = varietes.filter(Varieties.liste==liste)
    
    varietes = varietes.all()
    results = []
    for variete in varietes:    
        results.append({'id_espece': variete.id_espece, 'espece':variete.espece, 'id_variete': variete.id_variete, 'variete': variete.variete, 'liste': variete.liste, 'obtenteur': variete.obtenteur, 'annee_inscription': variete.annee_inscription, 'date_inscription': variete.date_inscription, 'informations_complementaires': variete.informations_complementaires, 'typ_var1': variete.typ_var1, 'typ_var2': variete.typ_var2, 'typ_var3': variete.typ_var3, 'typ_var4': variete.typ_var4, 'typ_var5': variete.typ_var5, 'code_gnis': variete.code_gnis})
    return jsonify(results)

@app.route('/varietes/<string:code_gnis>', methods=['GET'])
def get_variete_by_gnis(code_gnis):
    variete = Varieties.query.filter_by(code_gnis=code_gnis).first()
    if variete:
        result = {'id_espece': variete.id_espece, 'espece':variete.espece, 'id_variete': variete.id_variete, 'variete': variete.variete, 'liste': variete.liste, 'obtenteur': variete.obtenteur, 'annee_inscription': variete.annee_inscription, 'date_inscription': variete.date_inscription, 'informations_complementaires': variete.informations_complementaires, 'typ_var1': variete.typ_var1, 'typ_var2': variete.typ_var2, 'typ_var3': variete.typ_var3, 'typ_var4': variete.typ_var4, 'typ_var5': variete.typ_var5, 'code_gnis': variete.code_gnis}
        return jsonify(result)
    else:
        abort(404, {'message': 'Variete not found'})

@app.route('/especes', methods=['GET'])
def get_species():
    species = db.session.query(Varieties.id_espece, Varieties.espece).order_by(Varieties.espece).distinct().all()
    results = []
    for id_espece, espece in species:
        results.append({'id_espece': id_espece, 'espece': espece})
    return jsonify(results)

@app.route('/obtenteurs', methods=['GET'])
def get_obtenteurs():
    obtenteurs = db.session.query(Varieties.obtenteur).distinct().order_by(Varieties.obtenteur)
    results = [obtenteur[0] for obtenteur in obtenteurs]
    return jsonify(results)

@app.route('/listes', methods=['GET'])
def get_listes():
    listes = db.session.query(Varieties.liste).distinct().order_by(Varieties.liste)
    results = [liste[0] for liste in listes]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)