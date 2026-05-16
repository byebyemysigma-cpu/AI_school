import os
import re
import subprocess

print("🔥 TEST RENDER UNIQUE 🔥")

print("📚 Nombre exercices chargés :", len(exercices))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(BASE_DIR, "manuel_maths", "pages")

def lire_pages():
    exercices = lire_pages()

    print("📁 DOSSIER =", DOSSIER)
    print("📁 EXISTE =", os.path.exists(DOSSIER))
    
    for root, dirs, files in os.walk(DOSSIER):
        for fichier in files:
            if fichier.endswith(".txt"):
                chemin = os.path.join(root, fichier)

                with open(chemin, "r", encoding="utf-8") as f:

                    contenu = f.read().lower()

                    blocs = re.split(r"(exercice \d+ ?\:)", contenu)

                    for i in range(1, len(blocs), 2):
                        titre = blocs[i]
                        texte = blocs[i+1]

                        exercices.append({
                            "fichier": fichier,
                            "titre": titre,
                            "contenu": texte
                        })

    return exercices

def chercher_page_exo(page, numero, exercices):
    page = page.strip()
    numero = numero.strip()

    for exo in exercices:
        fichier = exo["fichier"]

        print("📄 Fichier :", fichier)
        print("📘 Page demandée :", page)
        print("🧠 Titre exercice :", exo["titre"])
        
        # 🔥 vérifier la page dans le NOM DU FICHIER (beaucoup plus fiable)
        if page in fichier:
            if f"exercice {numero}" in exo["titre"]:
                print("\n📘 Exercice trouvé !")
                print("📄 Fichier :", fichier)
                print(exo["titre"])
                print(exo["contenu"][:300])
                return exo

    print("❌ Exercice introuvable")
    return None

# ---------- CALCUL ----------
def extraire_calculs(texte):
    pattern = r"[-+]?\d+[.,]?\d*\s*[\+\-\*/x×÷]\s*[-+]?\d+[.,]?\d*"
    return re.findall(pattern, texte)

def calculer(expression):
    try:
        expression = expression.replace(",", ".")
        expression = expression.replace("×", "*").replace("÷", "/")
        return eval(expression)
    except:
        return "Erreur"

def resoudre_exercice(exo):
    contenu = exo["contenu"]

    print("\n🧠 Résolution :")

    calculs = extraire_calculs(contenu)

    if len(calculs) == 0:
        print("👉 Aucun calcul détecté")
        return

    for calc in calculs:
        print(calc, "=", calculer(calc))

# ---------- IMAGE ----------
def afficher_image(page):
    page = int(page)

    # 🔍 trouver le bon dossier (ex: 50-59)
    for dossier in os.listdir(DOSSIER):
        if "-" in dossier:
            debut, fin = dossier.split("-")

            if int(debut) <= page <= int(fin):
                chemin_dossier = os.path.join(DOSSIER, dossier)

                # 🔍 chercher image dans ce dossier
                for fichier in os.listdir(chemin_dossier):
                    if fichier.lower().endswith((".jpg", ".png")):
                        if str(page) in fichier:
                            chemin_image = os.path.join(chemin_dossier, fichier)

                            print("🖼️ Image trouvée :", chemin_image)
                            
                            subprocess.run(["start", "", chemin_image], shell=True)
                            return

    print("❌ Image non trouvée pour la page", page)

def construire_pages_exercices(exercices):

    pages_exercices = {}

    for exo in exercices:

        contenu = exo["contenu"]

        match_page = re.search(r"page\s*:?\s*(\d+)", contenu)

        if match_page:

            page = match_page.group(1)

            numeros = re.findall(r"exercice\s*(\d+)", contenu)

            if page not in pages_exercices:
                pages_exercices[page] = []

            for num in numeros:

                if num not in pages_exercices[page]:
                    pages_exercices[page].append(num)

    return pages_exercices

def trouver_exercices_page(page):

    exercices = []

    for root, dirs, files in os.walk(DOSSIER):

        for fichier in files:

            # 🔥 uniquement txt
            if not fichier.endswith(".txt"):
                continue

            nom = fichier.lower()

            # 🔥 vérifier si la page est dans le nom
            if page in nom:

                chemin = os.path.join(root, fichier)

                with open(chemin, "r", encoding="utf-8") as f:

                    contenu = f.read().lower()

                    # 🔥 trouver les exercices
                    numeros = re.findall(r"exercice\s+(\d+)", contenu)

                    for num in numeros:

                        if num not in exercices:
                            exercices.append(num)

        return exercices
    