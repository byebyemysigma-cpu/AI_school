from flask import Flask, request
import os


app = Flask(__name__)

exercices = []



historique = []


@app.route("/", methods=["GET", "POST"])
def accueil():

    resultat = ""

    if request.method == "POST":

        page = request.form["page"]
        exercice = request.form["exercice"]

        exo = chercher_page_exo(page, exercice, exercices)

        if exo:

            description = exo["contenu"][:1000]
            historique.append(f"📘 Page {page} • Exercice {exercice}")
            resultat = f"""
            <h2>📘 Exercice trouvé</h2>

            <p><b>Fichier :</b> {exo["fichier"]}</p>

            <pre>{description}</pre>
            """

        else:

            resultat = "<p>❌ Exercice introuvable</p>"

    return f"""

<html>

<head>

<title>IA School</title>

<style>

body {{
    background-color: #0f0f0f;
    color: white;
    font-family: Arial;
    margin: 0;
}}

.topbar {{
    background-color: #1a1a1a;
    padding: 15px;
    text-align: center;
    border-bottom: 1px solid #333;
}}

.main {{
    padding: 40px;
    min-height: 70vh;
}}

.result {{
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 10px;
    white-space: pre-wrap;
}}

.bottombar {{
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #1a1a1a;
    padding: 20px;
    border-top: 1px solid #333;
}}

input {{
    padding: 10px;
    margin-right: 10px;
    border-radius: 5px;
    border: none;
}}

button {{
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #3b82f6;
    color: white;
    cursor: pointer;
}}

button:hover {{
    background-color: #2563eb;
}}

</style>

</head>

<body>

<div class="topbar">
    <h2>IA School</h2>
    <p>créé par wo • Assistant </p>
</div>

<div class="main">

    <div class="result">

        {resultat}

        <br><br>

        <h3>📜 Historique</h3>

        {"<br>".join(historique)}

    </div>

</div>

<div class="bottombar">

<form method="POST">
<input type="text" name="page" placeholder="Page">

<input type="text" name="exercice" placeholder="Exercice">
    <button type="submit">Chercher</button>

</form>

</div>

</body>

</html>

"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)