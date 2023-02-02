import os
import hashlib
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# URL de téléchargement du fichier CSV
url = "https://www.semae.fr/wp-admin/admin-ajax.php?action=exportCsv&espece=&variete=&liste=&search="

# Chemin du fichier CSV local
file_path = "varieties.csv"

# Hachage du fichier existant (s'il existe)
old_hash = ""
if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        old_hash = hashlib.sha1(data).hexdigest()

# Téléchargement du fichier CSV
try:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    new_file = response.content
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("Something went wrong:",err)

# Hachage du nouveau fichier
new_hash = hashlib.sha1(new_file).hexdigest()

# Si les hash ne sont pas égaux, mise à jour des données en base de données
if old_hash != new_hash:
    # Enregistrement du nouveau fichier
    with open(file_path, "wb") as f:
        f.write(new_file)

    # Connexion à la base de données
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    else:
        cur = conn.cursor()

        # Copie des données à partir du fichier CSV
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                cur.copy_expert("COPY {} (id_espece, espece, id_variete, variete, liste, obtenteur, annee_inscription, date_inscription, informations_complementaires, typ_var1, typ_var2, typ_var3, typ_var4, typ_var5, code_gnis, blank) FROM STDIN WITH (FORMAT CSV, DELIMITER ';', HEADER)".format(os.getenv('DB_TABLE')), f)
            conn.commit()

        except psycopg2.Error as e:
            print(f"Error copying data from CSV: {e}")

        finally:
            # Fermeture de la connexion
            cur.close()
            conn.close()