# Objectifs

Ce projet a pour objectif de créer une API sur la base des variétés de SEMAE. 
https://www.semae.fr/catalogue-varietes/base-varietes-gnis/

> Disclaimer juridique sur les donnnées : 
Sont accessibles : l’intégralité des variétés des listes du Catalogue national et les variétés inscrites dans d’autres pays de l’Union européenne qui sont produites et/ou commercialisées en France (soit plus de 17 000 variétés).
Les informations présentées ne revêtent aucune valeur juridique, seul fait foi la publication au Journal officiel français ou de l’Union européenne.

Sur la base d'un fichier CSV disponible, les données sont importées dans une base de données puis exposées à travers une API Python, créé à l'aide de Flask.

Plusieurs points d'entrées sont disponibles :

 - /varietes => permet de récupérer toutes les informations de toutes les variétés. Il est possible de filtrer cette liste par espèce (à l'aide de l'identifiant id_espece), par obtenteur (à l'aide du nom de l'obtenteur), par liste (à l'aide du nom de la liste), ou encore de faire une recherche textuelle (à l'aide du nom de la variété).
 - /varietes/{code_GNIS} => permet de récupérer toutes les informations d'une variété dont le code GNIS est précisé en paramètre
 - /obtenteurs => retourne la liste de tous les obtenteurs 
 - /listes => retourne toutes les listes sur lesquelles les variétés peuvent être inscrites
 - /especes => retourne toutes les espèces avec leurs identifiants et leurs libellés

Technologies utilisées :
- Un serveur pour héberger les applicatifs ;
- PostgreSQL (version 15.0 utilisé) ;
- Python 3.11.1

# Installation manuelle

## Base de données

Nous avons fait le choix de stocker les données dans une base PostgreSQL.
Si ce n'est pas encore le cas, commencer par installer le serveur PostgreSQL
Créer un utilisateur et une base de données dédié.
Créer la table "Varietes"

    CREATE TABLE varietes (
        id_espece VARCHAR(255),
        espece VARCHAR(255),
        id_variete VARCHAR(255),
        variete VARCHAR(255),
        liste VARCHAR(255),
        obtenteur VARCHAR(255),
        annee_inscription INTEGER,
        date_inscription DATE,
        informations_complementaires TEXT,
        typ_var1 VARCHAR(255),
        typ_var2 VARCHAR(255),
        typ_var3 VARCHAR(255),
        typ_var4 VARCHAR(255),
        typ_var5 VARCHAR(255),
        code_gnis VARCHAR(255),
        blank VARCHAR(255)
    );

La colonne blank est obligatoire car le fichier csv sur lequel nous nous basons termine ses lignes par un séparateur. 

> Attention, vérifer que la table appartient bien à votre utilisateur dédié et non à postgres. Cela peut arriver si vous passer par PgAdmin par exemple.

## Variables d'environnement

Définir les variables d'environnement correspondant à votre système dans un fichier .env
    DB_HOST=''
    DB_PORT=''
    DB_USER=''
    DB_PASSWORD=''
    DB_NAME=''
    DB_TABLE='varietes'

## Peuplement des données

Récupérer les fichiers du projet 
Si nécessaire installer python et les dépendances nécessaires au fonctionnement du projet 

    python3 pip install -r requirements.txt

Lancer le script get_data.py pour la première fois

    python3 get_data.py
Vérifier que les données sont présentes en base de données via PgAdmin ou via psql

## Lancement de l'API

Pour démarrer l'API, exécuter la commande suivante :

    python3 api.py

L'API se lancera sur l'url localhost:5000
Vous pourrez la tester sur l'URL localhost:5000/varietes

Pour exposer l'URL sur une autre URL, vous pouvez utiliser un reverse proxy comme NGINX - non détaillé dans ce readme. 

## Mise en place de la mise à jour des données

Ajouter un cron job pour lancer le get_data selon une périodicité à définir.
Editer le fichier crontab en exécutant la commande `crontab -e` et d'ajouter la ligne suivante :

`0 7 * * * python3 /chemin/vers/get_data.py`

# Dockerisation et automatisation
En cours, n'hésitez pas à me contacter pour échanger si vous le souhaitez


