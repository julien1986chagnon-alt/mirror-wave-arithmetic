def division_tableau_automatique(n, x):
    """Calcule dynamiquement la valeur de la table sans base de données."""
    if x == 1:
        return n
    if x < n:
        return n - x
    return 9 - x + n

def convertir_en_base_9_sans_zero(nombre_base_10):
    """Convertit un score total d'une colonne dans votre système sans zéro."""
    if nombre_base_10 == 0:
        return ""
    
    resultat = ""
    while nombre_base_10 > 0:
        reste = nombre_base_10 % 9
        if reste == 0:
            resultat = "9" + resultat
            nombre_base_10 = (nombre_base_10 // 9) - 1
        else:
            resultat = str(reste) + resultat
            nombre_base_10 = nombre_base_10 // 9
            
    return resultat

def addition_base_9_pure(blocs):
    """Effectue l'addition colonne par colonne selon vos règles."""
    max_len = max(len(b) for b in blocs)
    blocs_padded = [b.zfill(max_len) for b in blocs]
    
    resultat_final = ""
    retenue = 0
    
    # On progresse de droite à gauche
    for i in range(max_len - 1, -1, -1):
        somme_colonne_10 = retenue + sum(int(b[i]) for b in blocs_padded)
        
        if i == 0:
            conversion = convertir_en_base_9_sans_zero(somme_colonne_10)
            resultat_final = conversion + resultat_final
        else:
            conversion = convertir_en_base_9_sans_zero(somme_colonne_10)
            chiffre_unites = conversion[-1]
            chiffre_retenue = conversion[:-1]
            
            resultat_final = chiffre_unites + resultat_final
            retenue = int(chiffre_retenue) if chiffre_retenue else 0
            
    return resultat_final

def calculette_interactive_detaillee(nombre1, nombre2):
    N_str = str(nombre1)
    X_str = str(nombre2)
    blocs = []
    
    print("\n--- DECOMPOSITION DU CALCUL ---")
    
    # Étape 1 : Division chiffre par chiffre avec explications
    for chiffre_N in N_str:
        bloc_actuel = ""
        explications = []
        for chiffre_X in X_str:
            res = division_tableau_automatique(int(chiffre_N), int(chiffre_X))
            bloc_actuel += str(res)
            explications.append(f"{chiffre_N} / {chiffre_X} = {res}")
        
        print(f"Pour le chiffre {chiffre_N} : {', '.join(explications)} -> Bloc : {bloc_actuel}")
        blocs.append(bloc_actuel)
    
    # Étape 2 : Présentation visuelle de l'addition
    print("\n--- ADDITION FINALE ---")
    max_len = max(len(b) for b in blocs)
    for b in blocs:
        print(f" {b.zfill(max_len)}")
    print(" " + "-" * max_len)
    
    # Étape 3 : Calcul du résultat
    reponse = addition_base_9_pure(blocs)
    print(f"= {reponse}")
    return reponse

# ==========================================
# BOUCLE PRINCIPALE
# ==========================================
print("=== BIENVENUE DANS VOTRE CALCULETTE SPECIALE BASE 9 ===")
print("(Pour quitter, tapez 'quitter')\n")

while True:
    n1_input = input("Entrez le premier nombre (ex: 153) : ").strip()
    if n1_input.lower() == 'quitter':
        break
        
    n2_input = input("Entrez le deuxième nombre (ex: 149) : ").strip()
    if n2_input.lower() == 'quitter':
        break

    if not n1_input.isdigit() or not n2_input.isdigit() or '0' in n1_input or '0' in n2_input:
        print("Erreur : Veuillez entrer uniquement des nombres entiers sans le chiffre 0.\n")
        continue

    try:
        calculette_interactive_detaillee(n1_input, n2_input)
        print("\n" + "="*40 + "\n")
    except Exception as e:
        print(f"Une erreur est survenue lors du calcul : {e}\n")
