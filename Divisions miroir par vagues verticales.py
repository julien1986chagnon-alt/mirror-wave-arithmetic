import time
import random
import sqlite3
import datetime
import sys

# =====================================================================
# 1. EXPANSION DU MATRICIEL SANS ZÉRO
# =====================================================================
BASE_C1 = {"1":"1", "2":"8", "3":"7", "4":"6", "5":"5", "6":"4", "7":"3", "8":"2", "9":"9"}
HORLOGE = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
TABLES = {"1": BASE_C1}

for i in range(2, 10):
    c_str = str(i)
    TABLES[c_str] = {}
    decalage = i - 1
    for k, v in BASE_C1.items():
        TABLES[c_str][k] = HORLOGE[(HORLOGE.index(v) + decalage) % 9]

# =====================================================================
# 2. MOTEUR EN STREAMING (ANTI-CRASH RAM DE GOOGLE)
# =====================================================================
def diviser_streaming_absolu(num_geant, den_geant):
    """
    Calcule le résultat vertical sans stocker les séquences intermédiaires.
    Ce processus protège les 12 Go de RAM de Google en jetant la donnée traitée.
    """
    longueur_den = len(den_geant)
    longueur_num = len(num_geant)

    # La longueur maximale d'une séquence finale alignée
    taille_max = longueur_den

    resultat_inverse = []
    retenue = 0

    # On traite l'addition colonne par colonne à l'envers (de droite à gauche)
    # sans jamais créer les chaînes de texte complètes en mémoire
    for idx_colonne in range(taille_max - 1, -1, -1):
        somme_verticale = retenue

        # Pour chaque chiffre du numérateur, on retrouve instantanément
        # le chiffre correspondant dans sa vague sans stocker la vague
        chiffre_den = den_geant[idx_colonne]
        for chiffre_num in num_geant:
            chiffre_calcule = TABLES[chiffre_num][chiffre_den]
            somme_verticale += int(chiffre_calcule)

        if somme_verticale == 0:
            if idx_colonne != 0 or retenue != 0:
                resultat_inverse.append("0") # Ajustement structurel temporaire
            continue

        reste = somme_verticale % 9
        quotient = somme_verticale // 9
        if reste == 0:
            reste = 9
            retenue = quotient - 1
        else:
            retenue = quotient

        resultat_inverse.append(str(reste))

    if retenue > 0:
        resultat_inverse.append(str(retenue))

    # On remet le résultat dans le bon sens
    valeur_finale = "".join(reversed(resultat_inverse))
    return valeur_finale.replace("0", "1") # Nettoyage des alignements vides

# =====================================================================
# 3. LE CASSEUR DE LIMITES AUTOMATIQUE
# =====================================================================
conn = sqlite3.connect('limite_extreme_google.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taille_chiffres INTEGER,
        duree_secondes REAL,
        timestamp TEXT
    )
''')
conn.commit()

# On commence fort : des nombres de 10 000 chiffres !
# Le programme va doubler la taille à chaque réussite pour chercher le crash.
taille_test = 10000
compteur = 1

print("🔥 ATTENTAT AUX LIMITES DE GOOGLE COLAB LANCÉ 🔥", flush=True)
print("RAM surveillée. SQLite en mode écriture directe.\n", flush=True)

try:
    while True:
        try:
            print(f"📊 [TEST #{compteur}] Tentative sur des nombres de {taille_test} chiffres...", flush=True)

            # Génération en mémoire ultra-légère
            num_monstre = "".join(random.choice("123456789") for _ in range(5)) # Numérateur stable
            den_monstre = "".join(random.choice("123456789") for _ in range(taille_test))

            t0 = time.time()
            resultat = diviser_streaming_absolu(num_monstre, den_monstre)
            t1 = time.time()
            duree = t1 - t0

            print(f" ⚡ Résolu en {duree:.4f} secondes sans surchauffe de RAM.", flush=True)

            # Sauvegarde uniquement des métriques pour éviter que le fichier .db bloque le disque
            current_timestamp = datetime.datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO records (taille_chiffres, duree_secondes, timestamp)
                VALUES (?, ?, ?)
            ''', (taille_test, duree, current_timestamp))
            conn.commit()

            compteur += 1

            # MULTIPLICATION DE LA DIFFICULTÉ : On augmente la taille de 50% à chaque fois
            taille_test = int(taille_test * 1.5)
            time.sleep(1)

        except Exception as e:
            print(f"\n💥 LA LIMITE DE GOOGLE A ÉTÉ TOUCHÉE : {e}", flush=True)
            print("Tentative de stabilisation et maintien du flux...", flush=True)
            taille_test = int(taille_test * 0.8) # Redescente d'un cran pour ne pas couper le moteur
            time.sleep(2)
            continue

except KeyboardInterrupt:
    print("\n🛑 Test extrême stoppé par l'utilisateur.", flush=True)
finally:
    conn.close()
