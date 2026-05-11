import tkinter as tk
from main import *

exercices = lire_pages()

def chercher():
    page = entry_page.get()
    exo_num = entry_exo.get()

    exo = chercher_page_exo(page, exo_num, exercices)

    if exo:
        afficher_image(page)
        resoudre_exercice(exo)

# fenêtre
fenetre = tk.Tk()

fenetre.title("IA School")
fenetre.geometry("500x400")

# texte
titre = tk.Label(fenetre, text="IA School", font=("Arial", 20))
titre.pack(pady=20)

# page
label_page = tk.Label(fenetre, text="Numéro de page")
label_page.pack()

entry_page = tk.Entry(fenetre)
entry_page.pack()

# exercice
label_exo = tk.Label(fenetre, text="Numéro de l'exercice")
label_exo.pack()

entry_exo = tk.Entry(fenetre)
entry_exo.pack()

# bouton
bouton = tk.Button(fenetre, text="Chercher", command=chercher)
bouton.pack(pady=20)

# boucle
fenetre.mainloop()

